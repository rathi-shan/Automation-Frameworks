import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import org.testng.annotations.Test;

public class ExtentReportPractice {
    @Test
    public void createReport() {
        // 1. Initialize the reporter
        ExtentSparkReporter spark = new ExtentSparkReporter("target/Spark.html");
        ExtentReports extent = new ExtentReports();
        extent.attachReporter(spark);

        // 2. Create a test
        ExtentTest test = extent.createTest("Login Test");
        test.pass("Application launched");
        test.info("Username entered");
        test.pass("Login successful");

        // 3. Flush the report (Mandatory to save it)
        extent.flush();
    }
}