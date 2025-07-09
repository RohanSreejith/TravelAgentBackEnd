document.addEventListener('DOMContentLoaded', function() {
    // Dashboard specific functionality
    
    // Package search form submission
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const destination = document.getElementById('id_destination');
            const duration = document.getElementById('id_duration_days');
            
            if (!destination.value.trim()) {
                e.preventDefault();
                destination.focus();
                return false;
            }
            
            if (!duration.value || duration.value < 1) {
                e.preventDefault();
                duration.focus();
                return false;
            }
            
            // Show loading indicator
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
        });
    }
    
    // Download JSON button
    const downloadBtn = document.querySelector('.download-json');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            // In a real app, this would fetch the data and create a download
            // For now, we'll just simulate it
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Preparing download...';
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-check"></i> Download complete';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-download"></i> Download Results';
                }, 2000);
            }, 1500);
        });
    }
    
    // Website form validation
    const websiteForm = document.querySelector('.website-form');
    if (websiteForm) {
        websiteForm.addEventListener('submit', function(e) {
            const name = document.getElementById('id_name');
            const url = document.getElementById('id_url');
            
            if (!name.value.trim()) {
                e.preventDefault();
                name.focus();
                return false;
            }
            
            if (!url.value.trim()) {
                e.preventDefault();
                url.focus();
                return false;
            }
            
            // Simple URL validation
            try {
                new URL(url.value);
            } catch (_) {
                e.preventDefault();
                alert('Please enter a valid URL (e.g., https://example.com)');
                url.focus();
                return false;
            }
        });
    }
    
    // Package form validation
    const packageForm = document.querySelector('.package-form');
    if (packageForm) {
        packageForm.addEventListener('submit', function(e) {
            const title = document.getElementById('id_title');
            const destination = document.getElementById('id_destination');
            const duration = document.getElementById('id_duration_days');
            const price = document.getElementById('id_price');
            
            if (!title.value.trim()) {
                e.preventDefault();
                title.focus();
                return false;
            }
            
            if (!destination.value.trim()) {
                e.preventDefault();
                destination.focus();
                return false;
            }
            
            if (!duration.value || duration.value < 1) {
                e.preventDefault();
                duration.focus();
                return false;
            }
            
            if (!price.value || price.value <= 0) {
                e.preventDefault();
                price.focus();
                return false;
            }
        });
    }
});