package utils;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class TestDataUtility {
    public static Map<String, String> generateContractData(){
        Map<String, String> data = new HashMap<>();
        String uniqueID = UUID.randomUUID().toString();

        data.put("contractId", "CONT-" + uniqueID.substring(0,8));
        data.put("customerName", "Accenture_Tester-" + System.currentTimeMillis());
        data.put("status", "PENDING");

        return data;

    }
}
