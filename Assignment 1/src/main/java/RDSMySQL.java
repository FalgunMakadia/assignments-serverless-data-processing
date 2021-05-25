// Assignment 1 - Part C

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicSessionCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.S3Object;

import java.io.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Hashtable;
import java.util.Scanner;

public class RDSMySQL
{

    static String accesskey = "ASIA5KWEVBPZRACYC3FI";
    static String secretkey = "Q7qnHC9gMXcuTXkRzQoGLLvmwkEhpTgGknm80bG6";
    static String sessiontoken = "IQoJb3JpZ2luX2VjEAUaCXVzLXdlc3QtMiJGMEQCIGrOuSkKchmOqlwZLxZ++uLCI62vgdEdnRElV7KNdSJRAiAildtAz+Wzc7W5vpxkdWKvh0gKbwFbfmqB5KqfobPxWiqxAgie//////////8BEAAaDDkxNjMxNDE5Njk3OSIMRFFdeo9G9u6hzGcdKoUCC7W5ilhTEsiacP+iyfHkWr3RO7mcaoLIXbZpvPSvYsSsVewsasbDskNMEUUa4OHWAUPNVNPLyauzBehHr0nStxYvASSs1/e8/M+cPbQd7YUKwbG75GBNN4ozAj6Pivja0D9cr86/Y3VTaZU/CTDvNg1asQM2mZcPgd6xjidCuSnkW5PkNidm25Zrznuy8hT+JLl9ncjtsQQRLUBWsm9aTB3J3MtznwBmv+mmxRADKQA0B/pyWCM04xVhVRSl1qD9gMc51cJNtXNgEC3lF/wxevJt6CurFEgly+b8AZLbYX3Jd1zqas6aVRcmwskTadIQX5zHVeoTo1eVhvSSSA8vmg6dLO79MKf4nIUGOp4BlcNjOzaydKJEKGLn7pB0SjJH0ZnjsjcdkJEAboCnK0/gwcCoRC4PSdEqQTK++bmB0ZslZsCJmH2qZYjFm5KIudXSCIyIGfDLnSubXA45+EnV5P85XDc6d4SAoutD34wM1TTEnmolqD6sqnVu3fTtqkJA7Bo4EhUUIoyvfgeLMDfTXwEnsH+fEKutPBs3tU7ZK42FwDzPMObHF2rmky8=";

    public static void main(String args[]) throws Exception
    {
        String url = "jdbc:mysql://a1-mysql-5410.c2kjexpbd5qy.us-east-1.rds.amazonaws.com:3306/5410_a1?autoReconnect=true&useSSL=false";
        String uname = "admin";
        String pass = "adminadmin";

        Class.forName("com.mysql.cj.jdbc.Driver");

        Connection Conn = DriverManager.getConnection(url, uname, pass);
        System.out.println("Connection Established.\n");

        Scanner sc = new Scanner(System.in);
        System.out.println("Welcome!");
        System.out.print("Enter 1 to Insert a Record and 2 to Fetch a Record by ID: ");
        int choice = sc.nextInt();

        if(choice == 1) {

            System.out.print("Enter ID: ");
            int id = sc.nextInt();
            System.out.print("Enter Password: ");
            String password = sc.next();

            String encryptedPassword = RDSMySQL.encryptPassword(password);
            System.out.println("Password Encryption Done!");

            String query = "INSERT INTO users VALUES(?,?)";
            PreparedStatement stmt = Conn.prepareStatement(query);

            stmt.setInt(1,id);
            stmt.setString(2,encryptedPassword);

            int i = stmt.executeUpdate();
            System.out.println(i + " Record Successfully Inserted!");

            stmt.close();

        } else if(choice == 2) {

            System.out.print("Enter ID to Fetch Password: ");
            int id = sc.nextInt();

            String query = "SELECT password FROM users WHERE id = ?";
            PreparedStatement stmt = Conn.prepareStatement(query);

            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();

            rs.next();
            String encryptedPassword = rs.getString("password");
            System.out.println("Encrypted Password For Given ID is : " + encryptedPassword);

            String decryptedPassword = RDSMySQL.decryptPassword(encryptedPassword);
            System.out.println("Decrypted Password For Given ID is : " + decryptedPassword);

            stmt.close();

        } else {

            System.out.println("Invalid Input!");

        }

        Conn.close();

    }

    public static Hashtable createEncryptionTable(){
        try
        {
            BasicSessionCredentials credentials = new BasicSessionCredentials(accesskey, secretkey, sessiontoken);

            AmazonS3 s3client = AmazonS3ClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(credentials)).withRegion(Regions.US_EAST_1).build();

            String bucketName = "bucket-lookup-table";
            String objectKey = "Lookup5410.txt";
            S3Object s3obj = s3client.getObject(new GetObjectRequest(bucketName, objectKey));

            BufferedReader reader = new BufferedReader(new InputStreamReader(s3obj.getObjectContent()));

            Hashtable<String, String> encryptionTable = new Hashtable<String, String>();

            String line;

            while ((line = reader.readLine()) != null)
            {
                String[] keyValuePair;
                keyValuePair = line.split("\t");
                encryptionTable.put(keyValuePair[0], keyValuePair[1]);
            }

            return encryptionTable;
        }
        catch(Exception e)
        {
            e.printStackTrace();
            return null;
        }
    }

    public static Hashtable createDecryptionTable(){
        try
        {
            BasicSessionCredentials credentials = new BasicSessionCredentials(accesskey, secretkey, sessiontoken);

            AmazonS3 s3client = AmazonS3ClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(credentials)).withRegion(Regions.US_EAST_1).build();

            String bucketName = "bucket-lookup-table";
            String objectKey = "Lookup5410.txt";
            S3Object object = s3client.getObject(new GetObjectRequest(bucketName, objectKey));

            BufferedReader reader = new BufferedReader(new InputStreamReader(object.getObjectContent()));

            Hashtable<String, String> decryptionTable = new Hashtable<String, String>();

            String line;

            while ((line = reader.readLine()) != null)
            {
                String[] keyValuePair;
                keyValuePair = line.split("\t");
                decryptionTable.put(keyValuePair[1], keyValuePair[0]);
            }

            return decryptionTable;
        }
        catch(Exception e)
        {
            e.printStackTrace();
            return null;
        }
    }

    public static String encryptPassword(String rawPassword) {
        Hashtable encryptionTable = RDSMySQL.createEncryptionTable();

        String encryptedPassword = "";

        for (int i = 0; i < rawPassword.length(); i++){
            char currentChar = rawPassword.charAt(i);
            String currentLetter = Character.toString(currentChar);
            String currentLetterEncrypted = (String) encryptionTable.get(currentLetter);
            encryptedPassword = encryptedPassword + currentLetterEncrypted;
        }

        return encryptedPassword;
    }

    public static String decryptPassword(String encryptedPassword) {
        Hashtable decryptionTable = RDSMySQL.createDecryptionTable();

        String decryptedPassword = "";

        for(int i = 0; i< encryptedPassword.length(); i = i+2){
            String currentChar1 = Character.toString(encryptedPassword.charAt(i));
            String currentChar2 = Character.toString(encryptedPassword.charAt(i+1));
            String currentLetterPair = currentChar1 + currentChar2;
            String currentLetterPairDecrypted = (String) decryptionTable.get(currentLetterPair);
            decryptedPassword = decryptedPassword + currentLetterPairDecrypted;
        }

        return decryptedPassword;
    }
}