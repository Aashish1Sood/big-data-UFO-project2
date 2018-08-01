import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.InputStream;
import java.io.PrintWriter;
import java.io.Reader;
import java.net.URL;
import java.util.Arrays;
import java.util.List;

import org.apache.tika.Tika;
import org.apache.tika.detect.Detector;
import org.apache.tika.parser.Parser;
import org.apache.tika.config.TikaConfig;
import org.apache.tika.io.IOUtils;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.image.ImageParser;
import org.apache.tika.parser.recognition.tf.TensorflowImageRecParser;
import org.apache.tika.sax.BodyContentHandler;


public class genCapAndObj {

	/**
	 * @param args
	 * @throws FileNotFoundException 
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		// Tika Configs used for using two dockers
		final String CONFIG_REST_FILE_OBJ_REC = "/home/aashish/tika1/tika/tika-parsers/src/test/resources/org/apache/tika/parser/recognition/tika-config-tflow-rest.xml";
		final String CONFIG_REST_FILE_IM2TXT = "/home/aashish/tika1/tika/tika-parsers/src/test/resources/org/apache/tika/parser/recognition/tika-config-tflow-im2txt-rest.xml";
		//String text = tika.parseToString(new File(CONFIG_REST_FILE_OBJ_REC));
		//System.out.print(text);
		
		
		TensorflowImageRecParser p = new TensorflowImageRecParser();
		//ImageParser imParser = new ImageParser();
		Parser parser = new AutoDetectParser();
		InputStream inputstreamObjRec = new FileInputStream(CONFIG_REST_FILE_OBJ_REC);
		InputStream inputstreamCap = new FileInputStream(CONFIG_REST_FILE_IM2TXT);
		
		Tika tikaObjRec = new Tika(new TikaConfig(inputstreamObjRec));
		Tika tikaCap = new Tika(new TikaConfig(inputstreamCap));
		
		Metadata metadata = new Metadata();
		String fname = "image_list";

		BufferedReader br = new BufferedReader(new FileReader(fname));
		int f_count = 0;
		int index = 200*f_count;
		String outFileName = "Featurized_output";
		InputStream imgStream = null;
		Reader reader;
		List<String> linesObjRec;
		List<String> linesCap;
		int count = 0;
		String val = String.valueOf(-1);
		
		//variable declaration for byte arrays to be used for streams
		ByteArrayOutputStream baos;
		ByteArrayInputStream bais;
		byte[] bytes;
		
		String[] md;// to store metadata keys
		String filePath = "./images/";
		String qualfname;
		String delim = ";;;"; //delimiter used for delimiting different features in metadata string
		//PrintWriter writer = new PrintWriter("results", "UTF-8");

		PrintWriter writer = new PrintWriter(new FileOutputStream(new File(outFileName), true /* append = true */));
		PrintWriter er_writer = new PrintWriter(new FileOutputStream(new File("Error_f"), true /* append = true */));
		List<String> metadata_string = Arrays.asList("gps", "date", "created", "caption", "object","content-type","location","model");
		StringBuilder metadataString;
		String line = "";
		int errCount =0;
		line = br.readLine();

		while (line != null) {
			try{
		        
		        //System.out.println(line);
		        
		        count+=1;
		        qualfname = filePath+line; // generate qualified filename
		        imgStream = new FileInputStream(new File(qualfname));
		        
		        //Below code is to save the Input stream in byteArray. which will be used again an again
		        baos = new ByteArrayOutputStream();
		        org.apache.commons.io.IOUtils.copy(imgStream, baos);
		        bytes = baos.toByteArray();
		        
		        //metadata features
		        bais = new ByteArrayInputStream(bytes);
		        metadata = new Metadata();
		        parser.parse(bais,new BodyContentHandler(),metadata, new ParseContext());

		        md = metadata.names();
		        metadataString = new StringBuilder("");
		        for(String name:md){
		        	for(String s_val: metadata_string){
		        		if (name.toLowerCase().startsWith(s_val)){
		        			//System.out.println(name+"="+metadata.get(name));
		        			metadataString.append(name+"="+metadata.get(name)+delim);
		        			break;
		        		}
		        	}
		        	
		        }
		        
		        //Object Recognition features
		        bais = new ByteArrayInputStream(bytes);
		        reader = tikaObjRec.parse(bais, metadata);
		        linesObjRec = IOUtils.readLines(reader);
		        //System.out.println(lines);
		        
		        // Image caption features
		        bais = new ByteArrayInputStream(bytes);
		        reader = tikaCap.parse(bais, metadata);
		        linesCap = IOUtils.readLines(reader);
		        
		        //Writing to file
		        writer.println(line);// Write To file the filename
		        writer.println(metadataString);
		        
		        if(linesObjRec.isEmpty()){
					//System.out.println("Nothing detected");
					writer.println(val);
				}
		        else{
		        	writer.println(linesObjRec);
		        	//System.out.println("Something detected");
		        }
		        
		        if(linesCap.isEmpty()){
					//System.out.println("Nothing detected");
					writer.println(val);
				}
		        else{
		        	writer.println(linesCap);
		        	//System.out.println("Something detected");
		        }
		        if(count%20 == 0){
		        	System.out.println(count);
		        }
		        
		        if(count>=6000)
		        	break;
		        line = br.readLine();
		        imgStream.close();
		    }
			catch (Exception e) {
			//e.printStackTrace();
			e.printStackTrace(er_writer);
			er_writer.println(line);
			er_writer.println(count);
			errCount+=1;
			line = br.readLine();
			imgStream.close();
		}
		finally {
			
		}

	}
		System.out.println("Closing all the streams");
		System.out.println(errCount);
		br.close();
	    writer.close();
	    er_writer.close();

}
}
