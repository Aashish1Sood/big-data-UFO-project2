import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.InputStream;
import java.io.PrintWriter;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashSet;

import org.apache.tika.Tika;
import org.apache.tika.config.TikaConfig;
import org.apache.tika.metadata.Metadata;


public class tikaNER {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		//NER Tika config
		final String CONFIG_NER = "./tika-config.xml";
		InputStream ner_config = new FileInputStream(CONFIG_NER);
		
		Tika tikaNER = new Tika(new TikaConfig(ner_config));
        
        String fname = "desc.txt"; // File containing textual information for each row
        BufferedReader br = new BufferedReader(new FileReader(fname));
        InputStream stream;
        HashSet<String> nerSet = new HashSet();
        nerSet.add("NER_PERSON");
        nerSet.add("NER_LOCATION");
        nerSet.add("NER_DATE");
        nerSet.add("NER_ORGANIZATION");
        int count = 2;
        String line = br.readLine();
        line = br.readLine();

        StringBuilder names;
        StringBuilder locs;
        StringBuilder orgs;
        StringBuilder dates;
        String f_str = "";
        
        // 4 NER fields will be generated in this TSV file
        PrintWriter writer = new PrintWriter(new FileOutputStream(new File("ner.tsv"), true /* append = true */));
        // Loop over each textual description
        while(line != null){
        	f_str = "";
        	names=new StringBuilder();locs=new StringBuilder();orgs=new StringBuilder();dates=new StringBuilder();
        	//System.out.println(line);
        	
        	if (line.trim() != ""){
        		Metadata metadata = new Metadata();
                tikaNER.parse(new ByteArrayInputStream(line.getBytes(Charset.defaultCharset())), metadata);
                String[] md = metadata.names();
                
                for(String name:md){
                	
                	//System.out.println(name+" "+metadata.get(name));
                	if(name.equals("NER_PERSON"))
                		{names.append(metadata.get(name));names.append(",");}
                	
                	if(name.equals("NER_LOCATION"))
                		{locs.append(metadata.get(name));names.append(",");}
                	
                	if(name.equals("NER_ORGANIZATION"))
                    	{orgs.append(metadata.get(name));names.append(",");}
                	
                    if(name.equals("NER_DATE"))
                        {;dates.append(metadata.get(name));names.append(",");}
                }
                f_str = names.toString()+"\t"+locs.toString()+"\t"+orgs.toString()+"\t"+dates.toString();
                //System.out.println(f_str);
                
        	}
        	
        	writer.println(f_str);
        	
            line = br.readLine();
            count+=1;
            if(count%50 == 0)
            	System.out.println(count);
        }
        writer.close();
	}

}
