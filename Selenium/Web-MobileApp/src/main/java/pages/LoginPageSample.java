package pages;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPageSample {
    WebDriver driver;
    By usernameField = By.id("user");
    By passwordField = By.id("password");
    By loginButton = By.id("login-btn");

    public LoginPageSample (WebDriver driver){
        this.driver = driver;
    }
    public void performLogin (String user, String pass){
        driver.findElement(usernameField).sendKeys(user);
        driver.findElement(passwordField).sendKeys(pass);
        driver.findElement(loginButton).click();

    }
}
