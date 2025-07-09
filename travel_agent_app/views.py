from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .forms import TravelAgentSignUpForm, TravelAgentLoginForm, WebsiteForm, TravelPackageForm, PackageSearchForm, PackageMediaFormSet
from .models import Website, TravelPackage, ScrapedPackage, PackageMedia
from .scrapers import get_scraper_for_website
import json
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from django.contrib import messages

@login_required
def delete_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk, agent=request.user)
    if request.method == 'POST':
        package.delete()
        return redirect('packages')
    return render(request, 'dashboard/confirm_delete.html', {'package': package})

@login_required
def edit_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk, agent=request.user)
    if request.method == 'POST':
        form = TravelPackageForm(request.POST, instance=package)
        formset = PackageMediaFormSet(request.POST, request.FILES, instance=package)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('package_detail', pk=package.pk)
    else:
        form = TravelPackageForm(instance=package)
        formset = PackageMediaFormSet(instance=package)
    return render(request, 'dashboard/edit_package.html', {
        'form': form,
        'formset': formset,
        'package': package
    })

@login_required
def package_detail(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'dashboard/package_detail.html', {'package': package})

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = TravelAgentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = TravelAgentSignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = TravelAgentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = TravelAgentLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')

@login_required
def packages(request):
    agent_packages = TravelPackage.objects.filter(agent=request.user)
    return render(request, 'dashboard/packages.html', {'packages': agent_packages})

@login_required
def add_package(request):
    if request.method == 'POST':
        form = TravelPackageForm(request.POST)
        formset = PackageMediaFormSet(request.POST, request.FILES, queryset=PackageMedia.objects.none())
        if form.is_valid() and formset.is_valid():
            package = form.save(commit=False)
            package.agent = request.user
            package.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.package = package
                instance.save()
            return redirect('packages')
    else:
        form = TravelPackageForm()
        formset = PackageMediaFormSet(queryset=PackageMedia.objects.none())
    return render(request, 'dashboard/add_package.html', {
        'form': form,
        'formset': formset
    })

@login_required
def profile(request):
    websites = Website.objects.filter(agent=request.user, is_active=True)
    
    if not websites.exists():
        from .signals import create_default_websites
        create_default_websites(TravelAgent, request.user, True)
        websites = Website.objects.filter(agent=request.user, is_active=True)
    
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save(commit=False)
            website.agent = request.user
            website.save()
            return redirect('profile')
    else:
        form = WebsiteForm()
    
    return render(request, 'dashboard/profile.html', {
        'websites': websites,
        'form': form
    })

@login_required
def delete_website(request, website_id):
    website = Website.objects.get(id=website_id, agent=request.user)
    website.is_active = False
    website.save()
    return redirect('profile')

@login_required
def search_packages(request):
    websites = Website.objects.filter(agent=request.user, is_active=True)
    if request.method == 'POST':
        form = PackageSearchForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            duration_days = form.cleaned_data['duration_days']
            max_price = form.cleaned_data['max_price']
            
            # Get all active websites for this agent
            websites = Website.objects.filter(agent=request.user, is_active=True)
            
            scraped_packages = []
            
            for website in websites:
                scraper = get_scraper_for_website(website.url)
                if scraper:
                    try:
                        packages = scraper.scrape(destination, duration_days, max_price)
                        for package in packages:
                            scraped_package = ScrapedPackage(
                                agent=request.user,
                                source_website=website,
                                title=package['title'],
                                destination=package['destination'],
                                duration_days=package['duration_days'],
                                price=package['price'],
                                description=package['description'],
                                original_url=package['url']
                            )
                            scraped_package.save()
                            scraped_packages.append(scraped_package)
                    except Exception as e:
                        print(f"Error scraping {website.name}: {str(e)}")
            
            return render(request, 'dashboard/results.html', {
                'packages': scraped_packages,
                'destination': destination,
                'duration_days': duration_days
            })
    else:
        form = PackageSearchForm()
    
    return render(request, 'dashboard/search.html', {
        'form': form,
        'websites': websites,
        'has_websites': websites.exists()  # Make sure this is passed
    })


@login_required
def download_results(request):
    destination = request.GET.get('destination', '')
    duration_days = request.GET.get('duration_days', '')
    
    packages = ScrapedPackage.objects.filter(
        agent=request.user,
        destination__icontains=destination,
        duration_days=duration_days
    ).order_by('price')
    
    data = []
    for package in packages:
        data.append({
            'title': package.title,
            'destination': package.destination,
            'duration_days': package.duration_days,
            'price': str(package.price),
            'description': package.description,
            'source_website': package.source_website.name,
            'url': package.original_url,
            'scraped_at': package.scraped_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="travel_packages_{destination}_{duration_days}days.json"'
    return response