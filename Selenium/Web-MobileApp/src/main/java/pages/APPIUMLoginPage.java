package pages;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.AppiumDriver;

public class APPIUMLoginPage {

    AppiumDriver driver;

    public APPIUMLoginPage(AppiumDriver driver) {

        this.driver = driver;
    }

    public void login(String user,
                      String pass) {

        driver.findElement(
            AppiumBy.accessibilityId(
                "username"))
            .sendKeys(user);

        driver.findElement(
            AppiumBy.accessibilityId(
                "password"))
            .sendKeys(pass);

        driver.findElement(
            AppiumBy.accessibilityId(
                "loginButton"))
            .click();
    }
}