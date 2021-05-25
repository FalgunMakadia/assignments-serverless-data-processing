// Assignment 1 - Part B

import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicSessionCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.*;

import java.io.File;

public class Bucket {

    String accesskey = "ASIA5KWEVBPZUC7VCUFD";
    String secretkey = "zASa9YjIzNVceRdHFq8eGNvqJtKO0gUJN89dr4Dv";
    String sessiontoken = "IQoJb3JpZ2luX2VjEDcaCXVzLXdlc3QtMiJIMEYCIQDSnpm0DgSZrV0ZZioE9O71GdBI7RhDaXmC03r42KAn4QIhAI0sTjUy+wb1BYg7ldvU4Y29Mouwr2Kh0y8lsjcfynZ6KrECCND//////////wEQABoMOTE2MzE0MTk2OTc5IgyM9UPUF0wcMa/vuu0qhQL6IyWsXxAxVoJLyJCYFQPc5pyl//4ISD1O95eipS0RKYzdLnAxRoQlO10UreC9O63v5UtjYZ+jP022ZxSHVQjHkQSY/9j11GLAJ10t9P0aa5MkzoK51suYR4Z5Fg86Q20Np1Bct81Bh/h96J9VpI2+i/GSPBv87L5l06tNfN5SqFLZKZKU+27EAbVjonDslr7GFTIv71jKkt0LowWqET2JBZZcYXF5wTIteEqGG1YG9el9YzVQx5xwyK3dZUxo2RmsapjjtAS7rdK5BnTW42NRDNoghJ2Yg3dGmCAuB7H8Mr3ZcCgbl6mzN2YrdpL/a0xosIw8FmxwYOWmx1EqiDuIUg2zdLgw+OqnhQY6nAHps0T2Yfl73nnmB+vIHYVcDsyXW+kY5E1eWSx0jK21IotbFhpBdjpHdaOYyBvoWKpaHjo94XG0h6PTQ24noZ5IQbg+z5jfgDGLx44tR9gd5q3lMJc1EjaK16cHI0+BsVDubZPzXwI4U3ru/j5dy6Ir7Fmkb0ARgaZ61zvxkuwZ8WUHSRKbeM5O1N6ht0cNTiMT+ij+kUClZqqf9mc=";

    BasicSessionCredentials credentials = new BasicSessionCredentials(accesskey, secretkey, sessiontoken);

    AmazonS3 s3client = AmazonS3ClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(credentials)).withRegion(Regions.US_EAST_1).build();

    public void saveFileToBucket(String bucketName, String fileNameOnBucket, String filePath) {

        s3client.putObject(bucketName, fileNameOnBucket, new File(filePath));

        System.out.println("File Saved to Bucket!");

    }

    public void createNewBucket(String bucketName){

        s3client.createBucket(bucketName);
        System.out.println("Bucket Successfully Created!");
        System.out.println("Bucket Name : " + bucketName);

    }

    public void disablePublicAccess(String bucketName){

        s3client.setPublicAccessBlock(new SetPublicAccessBlockRequest().withBucketName(bucketName).withPublicAccessBlockConfiguration(new PublicAccessBlockConfiguration().withBlockPublicAcls(true).withIgnorePublicAcls(true).withBlockPublicPolicy(true).withRestrictPublicBuckets(true)));
        System.out.println("Public Access has been Disabled for '"+ bucketName +"' Bucket.");

    }

    public void changeAclFullControlToOwner(String bucketName){

        Grant owner = new Grant(new CanonicalGrantee(s3client.getS3AccountOwner().getId()), Permission.FullControl);

        AccessControlList accessControlList = s3client.getBucketAcl(bucketName);
        accessControlList.grantAllPermissions(owner);

        s3client.setBucketAcl(bucketName, accessControlList);
        System.out.println("Granted Full Control to Bucket Owner!");

    }

    public void moveObjectAcrossS3(String fromBucketName, String toBucketName, String objectKey){

        try {

            s3client.copyObject(fromBucketName, objectKey, toBucketName, objectKey);
            s3client.deleteObject(fromBucketName, objectKey);
            System.out.println("File "+ objectKey +" Moved Successfully from Bucket " + fromBucketName + " to Bucket " + toBucketName);

        } catch (AmazonServiceException e) {
            System.out.println("File Moving Failed!");
            System.out.println(e.getErrorMessage());
            System.exit(1);
        }

    }
}
