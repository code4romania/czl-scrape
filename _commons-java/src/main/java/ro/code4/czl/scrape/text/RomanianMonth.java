package ro.code4.czl.scrape.text;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public enum RomanianMonth {

  IANUARIE(1),
  FEBRUARIE(2),
  MARTIE(3),
  APRILIE(4),
  MAI(5),
  IUNIE(6),
  IULIE(7),
  AUGUST(8),
  SEPTEMBRIE(9),
  OCTOMBRIE(10),
  NOIEMBRIE(11),
  DECEMBRIE(12);

  private final int number;

  RomanianMonth(int number) {
    this.number = number;
  }

  public int getNumber() {
    return number;
  }

  public static RomanianMonth fromLabel(String value) {
    switch (value.toLowerCase()) {
      case "ianuarie": {
        return IANUARIE;
      }
      case "februarie": {
        return FEBRUARIE;
      }
      case "martie": {
        return MARTIE;
      }
      case "aprilie": {
        return APRILIE;
      }
      case "mai": {
        return MAI;
      }
      case "iunie": {
        return IUNIE;
      }
      case "iulie": {
        return IULIE;
      }
      case "august": {
        return AUGUST;
      }
      case "septembrie": {
        return SEPTEMBRIE;
      }
      case "octombrie": {
        return OCTOMBRIE;
      }
      case "noiembrie": {
        return NOIEMBRIE;
      }
      case "decembrie": {
        return DECEMBRIE;
      }
      default: {
        throw new RuntimeException("Unrecognized month label " + value);
      }
    }
  }
}
