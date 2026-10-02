package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.subsystems.intake.IntakeSubsystem;

/**
 * Small command example: owns the intake while scheduled and stops it when interrupted.
 *
 * <p>The intake is still a no-op shell. Complete its TODO and tests before adding a button binding.
 */
public class IntakePracticeCommand extends Command {
  private final IntakeSubsystem intake;

  public IntakePracticeCommand(IntakeSubsystem intake) {
    this.intake = intake;
    addRequirements(intake);
  }

  @Override
  public void initialize() {
    intake.start();
  }

  @Override
  public void end(boolean interrupted) {
    // Runs when a button is released, another command needs the intake, or the robot is disabled.
    intake.stop();
  }

  @Override
  public boolean isFinished() {
    return false;
  }
}
