package hex.genmodel.attributes.parameters;

import java.util.Objects;

public class ParameterKey {
  
  private final String name;
  private final ParameterKey.Type type;
  private final String URL;

  public ParameterKey(String name, Type type, String URL) {
    Objects.requireNonNull(name);
    Objects.requireNonNull(type);
    Objects.requireNonNull(URL);

    this.name = name;
    this.type = type;
    this.URL = URL;
  }

  public enum Type {
    MODEL, FRAME, GENERIC
  }

  public String getName() {
    return name;
  }

  public Type getType() {
    return type;
  }

  public String getURL() {
    return URL;
  }
}
