import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import utils.ElementUtils;

public class SigninTest {
    public static void main(String[] args) {
        // 1. Initialize WebDriver
        WebDriver driver = new ChromeDriver();

        try {
            // 2. Navigate to the practice site
            driver.get("https://the-internet.herokuapp.com/login");

            // 3. Using By class to find elements
            // By.id is the fastest/most stable way to find elements
            WebElement usernameField = driver.findElement(By.id("username"));
            WebElement passwordField = driver.findElement(By.id("password"));
            WebElement loginButton = driver.findElement(By.tagName("button"));

            // 4. Perform actions
            usernameField.sendKeys("tomsmith");
            passwordField.sendKeys("SuperSecretPassword!");
            loginButton.click();

            // 5. Verification (Simple Print)
            System.out.println("Login button clicked successfully!");

        } finally {

            // 6. Cleanup
            driver.quit();
        }

        public void login(WebDriver driver) {
            ElementUtils utils = new ElementUtils(driver);

            // They don't need to write 'wait' code - it's baked into your library
            utils.clickElement(By.id("login-button"));
        }
    }
}