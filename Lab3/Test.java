import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

class Test{
    public static void main (String[] args){
        try{
            Path inputFile = Paths.get("Download.txt");
            byte[] inputBytes = Files.readAllBytes(inputFile);    
        

            Path outputFile = Paths.get("Junk.txt");
            Files.write(outputFile, inputBytes);    
        }
        catch (Exception e){
            e.printStackTrace();
        }

        System.out.println("Finished");
    }
}