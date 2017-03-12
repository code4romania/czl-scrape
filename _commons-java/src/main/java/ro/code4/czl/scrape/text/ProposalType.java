package ro.code4.czl.scrape.text;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public enum ProposalType {

  HG, LEGE, OM, OG, OUG, OTHER;

  public static ProposalType fromLabel(String label) {
    switch (label.toLowerCase()) {
      case "HG":
      case "hotarare": {
        return HG;
      }
      case "lege": {
        return LEGE;
      }
      case "om":
      case "ordin": {
        return OM;
      }
      case "og": {
        return OG;
      }
      case "oug": {
        return OUG;
      }
      default: {
        return OTHER;
      }
    }
  }

}
