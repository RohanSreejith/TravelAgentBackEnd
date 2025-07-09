import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
class ListenBtn implements ActionListener{ 
public void actionPerformed(ActionEvent e) { 

 System.out.println(e.getActionCommand());
 }
}
public class UISample implements ActionListener{
public static void main(String[] args) {
 JFrame f=new JFrame("Sample Window");
 f.setSize(500,500);
 f.setVisible(true);

 JLabel lblUser=new JLabel("User Name");
 lblUser.setBounds(30, 20, 80, 25);
 JTextField txtUser=new JTextField(20);
 txtUser.setBounds(120, 20, 200, 25);
 JButton b=new JButton("Click");
 b.setBounds(120, 90, 80, 25);
 f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE) ;
 f.setLayout(null);
 f.add(lblUser);
 f.add(txtUser);
 f.add(b);
 b.addActionListener(new UISample());

 }
public void actionPerformed(ActionEvent e) {
 System.out.println(e.getActionCommand());
    
}}







