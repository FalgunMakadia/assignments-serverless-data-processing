// Assignment 1 - Part B

public class BucketMain
{
    public static void main(String [] args)
    {
        System.out.println("Hello From Bucket Service!");

        String bucket1Name = "5410-a1-b1";
        String bucket2Name = "5410-a1-b2";
        String fileNameOnBucket = "Falgun.txt";
        String filePath = "src/main/resources/Falgun.txt";

        Bucket b1 = new Bucket();
        b1.saveFileToBucket(bucket1Name, fileNameOnBucket, filePath);
        b1.createNewBucket(bucket2Name);
        b1.disablePublicAccess(bucket2Name);
        b1.changeAclFullControlToOwner(bucket2Name);
        b1.moveObjectAcrossS3(bucket1Name, bucket2Name, fileNameOnBucket);

    }
}
