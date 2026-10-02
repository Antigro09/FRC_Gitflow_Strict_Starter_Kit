package frc.robot;

import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import frc.robot.commands.IntakePracticeCommand;
import frc.robot.subsystems.drive.DriveSubsystem;
import frc.robot.subsystems.intake.IntakeSubsystem;
import frc.robot.subsystems.shooter.ShooterSubsystem;
import frc.robot.subsystems.vision.VisionSubsystem;

/** Owns the subsystems and command bindings, following WPILib's command robot structure. */
public class RobotContainer {
  private final DriveSubsystem drive = new DriveSubsystem();
  private final IntakeSubsystem intake = new IntakeSubsystem();
  private final ShooterSubsystem shooter = new ShooterSubsystem();
  private final VisionSubsystem vision = new VisionSubsystem();

  public RobotContainer() {
    configureBindings();
  }

  private void configureBindings() {
    // Optional follow-up AFTER implementing intake and its tests:
    // 1. Create a CommandXboxController using Constants.OperatorConstants.DRIVER_CONTROLLER_PORT.
    // 2. Bind its A button with .whileTrue(createIntakePracticeCommand()).
    // Keep this starter unbound so startup never requests motion.
  }

  /** A command rookies can connect to a button after completing the intake exercise. */
  public Command createIntakePracticeCommand() {
    return new IntakePracticeCommand(intake);
  }

  /** Autonomous deliberately does nothing. */
  public Command getAutonomousCommand() {
    return Commands.none();
  }

  /** Clears all practice output requests when the robot is disabled. */
  public void stopAll() {
    drive.stop();
    intake.stop();
    shooter.stop();
  }

  /** Provides the simulated vision state for future command exercises. */
  public VisionSubsystem getVisionSubsystem() {
    return vision;
  }
}
