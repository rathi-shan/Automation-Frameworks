package api;

import static io.restassured.RestAssured.*;
import io.restassured.response.Response;

public class SportsAPI {
    public static Response getFollowedSports(String userId) {
        // Mocking the endpoint - in real life, this is your actual API URL
        return given()
                .header("Authorization", "Bearer token_abc")
                .when()
                .get("https://api.cbc.ca/sports/followed/" + userId);
    }
}