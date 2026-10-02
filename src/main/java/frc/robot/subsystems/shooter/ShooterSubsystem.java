package frc.robot.subsystems.shooter;

import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** Hardware-free shooter practice. This subsystem does not spin a real shooter. */
public final class ShooterSubsystem extends SubsystemBase {
  /**
   * Requests a target speed for the practice shooter.
   *
   * @param rpm requested revolutions per minute
   */
  public void setTargetRpm(double rpm) {
    // Rookie TODO: Add a private double field, initially 0.0. Clamp rpm to
    // [0.0, Constants.Practice.MAX_SHOOTER_RPM] and store the result.
    // Import frc.robot.Constants and test zero, 5000 RPM, and out-of-range values.
  }

  /** Returns the stored target speed once the rookie exercise is implemented. */
  public double getTargetRpm() {
    // Rookie TODO: Return the field you added in setTargetRpm().
    return 0.0;
  }

  /** Requests zero RPM. */
  public void stop() {
    setTargetRpm(0.0);
  }

  @Override
  public void periodic() {
    // Optional follow-up: Publish getTargetRpm() to SmartDashboard for simulation.
  }
}
