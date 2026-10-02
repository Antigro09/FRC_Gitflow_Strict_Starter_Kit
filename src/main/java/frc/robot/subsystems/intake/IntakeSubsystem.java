package frc.robot.subsystems.intake;

import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** Hardware-free intake practice. This subsystem does not control a real motor. */
public class IntakeSubsystem extends SubsystemBase {
  /** Starts the practice intake once the rookie exercise is implemented. */
  public void start() {
    // Rookie TODO: Add a private boolean field, initially false, and set it to true here.
  }

  /** Stops the practice intake once the rookie exercise is implemented. */
  public void stop() {
    // Rookie TODO: Set your running field to false. Calling stop() twice should be safe.
  }

  /** Returns whether the practice intake is running. */
  public boolean isRunning() {
    // Rookie TODO: Return your field. Test initial state, start(), stop(), and repeated calls.
    return false;
  }

  @Override
  public void periodic() {
    // Optional follow-up: Publish isRunning() to SmartDashboard for simulation.
  }
}
