package frc.robot.subsystems.drive;

import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** Hardware-free drive practice. This subsystem does not control a real drivetrain. */
public final class DriveSubsystem extends SubsystemBase {
  /**
   * Requests a speed for the practice drivetrain.
   *
   * @param speed requested speed, where -1.0 is full reverse and 1.0 is full forward
   */
  public void setRequestedSpeed(double speed) {
    // Rookie TODO: Add a private double field, initially 0.0. Clamp speed to [-1.0, 1.0]
    // and store the result. Test both endpoints, zero, and values outside the range.
  }

  /** Returns the stored requested speed once the rookie exercise is implemented. */
  public double getRequestedSpeed() {
    // Rookie TODO: Return the field you added in setRequestedSpeed().
    return 0.0;
  }

  /** Requests zero speed. */
  public void stop() {
    setRequestedSpeed(0.0);
  }

  @Override
  public void periodic() {
    // Optional follow-up: Publish getRequestedSpeed() to SmartDashboard for simulation.
  }
}
