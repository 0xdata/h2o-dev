package water.util;

import org.eclipse.jetty.io.EofException;
import water.Key;

import java.io.*;
import java.net.URI;
import java.net.URL;
import java.nio.file.Path;
import java.util.UUID;

/**
 * File utilities.
 */
public class FileUtils {
  /**
   * Silently close given files.
   *
   * @param closeable files to close
   */
  public static void close(Closeable...closeable) {
    for(Closeable c : closeable)
      try { if( c != null ) c.close(); } catch( IOException xe ) { }
  }

  public static void copyStream(InputStream is, OutputStream os, final int buffer_size) {
    try {
      byte[] bytes=new byte[buffer_size];
      while( is.available() > 0 )
      {
        int count=is.read(bytes, 0, buffer_size);
        if(count<=0)
          break;
        os.write(bytes, 0, count);
      }
    }
    catch(EofException eofe) {
      // no problem
    }
    catch(Exception ex) {
      throw new RuntimeException(ex);
    }
  }

  public static URI getURI(String path) {
    boolean windowsPath = path.matches("^[a-zA-Z]:.*$");
    if (windowsPath) {
      return new File(path).toURI();
    } else if (path.contains(":/")) { // Seems like
      return URI.create(path);
    } else {
      return new File(path).toURI();
    }
  }

  public static boolean delete(File file) {
    if (file.isFile())
      file.delete();
    else if (file.isDirectory()) {
      File[] files = file.listFiles();
      for (File f: files) {
        f.delete();
      }
      // Delete top-level directory
      return file.delete();
    }

    return false;
  }

  /** Transform given key to a string which can be used as a file name. */
  public static String keyToFileName(Key k) {
    return k.toString().replaceAll("[^a-zA-Z0-9_\\-\\.]", "_");
  }

  /** Transform an image URL to a valid local file **/
  public static String imageToUUID(String _file) {
    return UUID.nameUUIDFromBytes(_file.getBytes()).toString() + _file.substring(_file.length()-4,_file.length());
  }

  synchronized
  public static void downloadFile(URL url, Path path) throws IOException {
    InputStream is = url.openStream();
    OutputStream os = new FileOutputStream(path.toFile());
    byte[] b = new byte[2048];
    int length;
    while ((length = is.read(b)) != -1) {
      os.write(b, 0, length);
    }
    is.close();
    os.close();
  }

}
