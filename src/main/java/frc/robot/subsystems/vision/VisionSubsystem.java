package frc.robot.subsystems.vision;

import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** Hardware-free vision practice. This subsystem does not connect to a camera. */
public final class VisionSubsystem extends SubsystemBase {
  /**
   * Supplies a pretend camera observation for practice.
   *
   * @param visible whether the simulated target is visible
   */
  public void setSimulatedTargetVisible(boolean visible) {
    // Rookie TODO: Add a private boolean field, initially false, and store visible in it.
  }

  /** Returns the most recent simulated visibility once the rookie exercise is implemented. */
  public boolean hasTarget() {
    // Rookie TODO: Return your field. Test initial false, then true, then false again.
    return false;
  }

  @Override
  public void periodic() {
    // Optional follow-up: Publish hasTarget() to SmartDashboard for simulation.
  }
}
