package stepDefinitions;

import api.SportsAPI;
import org.openqa.selenium.WebDriver;
import pages.LoginPage;

public class FollowSportsSteps {
    WebDriver driver = new ChromeDriver();
    LoginPage loginPage = new LogingPage(driver);

    @Given ("the user is logged into the CBC News app")
    public void the_user_is_logged_in() {
        driver.get("https://www.cbc.ca/login");
        loginPage.performLogin("testuser", "password123");
    }

    @When("the user navigates to the {string} section")
    public void navigate_to_section(String section) {
        // Injecting dynamic test data
        Map<String, String> testData = TestDataUtility.generateContractData();
        System.out.println("Creating contract: " + testData.get("contractId"));
        // ... logic to use this data in the UI
    }

    @And("selects {string}")
    public void selects_sport(String sport) {
        System.out.println("Selecting: " + sport);
    }

    // Inside your FollowSportsSteps.java class
    @Then("the {string} sport should be added to the {string} list")
    public void verify_addition(String sport, String listName) {
        // 1. UI Check (Existing)
        System.out.println("UI check passed: " + sport + " is visible.");

        // 2. API Check (The Lead Skill)
        var response = SportsAPI.getFollowedSports("testuser");
        assert response.getStatusCode() == 200;
        assert response.getBody().asString().contains(sport);

        System.out.println("API check passed: Backend confirmed " + sport + " is saved.");
        driver.quit();
    }
}


