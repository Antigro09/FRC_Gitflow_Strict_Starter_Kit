package frc.robot;

/** Shared practice constants. Add real hardware IDs only when the team starts hardware work. */
public final class Constants {
  private Constants() {}

  /** Values for the hardware-free rookie exercises. */
  public static final class Practice {
    public static final double MAX_SHOOTER_RPM = 5000.0;

    private Practice() {}
  }

  /** Reserved for a future controller binding exercise. No controller is created yet. */
  public static final class OperatorConstants {
    public static final int DRIVER_CONTROLLER_PORT = 0;

    private OperatorConstants() {}
  }
}
