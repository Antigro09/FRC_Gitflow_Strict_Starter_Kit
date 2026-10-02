package frc.robot;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import edu.wpi.first.hal.HAL;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import edu.wpi.first.wpilibj2.command.Commands;
import frc.robot.commands.IntakePracticeCommand;
import frc.robot.subsystems.drive.DriveSubsystem;
import frc.robot.subsystems.intake.IntakeSubsystem;
import frc.robot.subsystems.shooter.ShooterSubsystem;
import frc.robot.subsystems.vision.VisionSubsystem;
import java.util.Set;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** Examples of testing command behavior without connecting any robot hardware. */
class RobotPracticeTest {
  private CommandScheduler scheduler;

  @BeforeAll
  static void initializeHal() {
    assertTrue(HAL.initialize(500, 0), "WPILib simulation must initialize before these tests");
  }

  @BeforeEach
  void prepareEnabledRobot() {
    scheduler = CommandScheduler.getInstance();
    resetScheduler();
    scheduler.enable();
    DriverStationSim.resetData();
    DriverStationSim.setDsAttached(true);
    DriverStationSim.setEnabled(true);
    DriverStationSim.notifyNewData();
  }

  @AfterEach
  void cleanUp() {
    resetScheduler();
    DriverStationSim.resetData();
    DriverStationSim.notifyNewData();
  }

  private void resetScheduler() {
    scheduler.cancelAll();
    scheduler.getActiveButtonLoop().clear();
    scheduler.clearComposedCommands();
    scheduler.unregisterAllSubsystems();
  }

  @Test
  void subsystemsBeginInSafeIdleStates() {
    assertEquals(0.0, new DriveSubsystem().getRequestedSpeed());
    assertFalse(new IntakeSubsystem().isRunning());
    assertEquals(0.0, new ShooterSubsystem().getTargetRpm());
    assertFalse(new VisionSubsystem().hasTarget());
    // Rookie exercise: add tests for your subsystem's new behavior in your own PR.
    // These checks describe startup only, so implementing the TODOs does not break them.
  }

  @Test
  void intakeCommandOwnsItsSubsystemAndStartsWhenScheduled() {
    TrackingIntake intake = new TrackingIntake();
    Command command = new IntakePracticeCommand(intake);

    assertEquals(Set.of(intake), command.getRequirements());
    assertEquals(0, intake.startCalls);
    scheduler.schedule(command);
    scheduler.run();

    assertTrue(command.isScheduled(), "The practice command should run until interrupted");
    assertTrue(intake.isRunning());
    assertEquals(1, intake.startCalls, "Starting happens once, not on every scheduler cycle");
    assertEquals(0, intake.stopCalls);
  }

  @Test
  void cancellingIntakeCommandStopsIntake() {
    TrackingIntake intake = new TrackingIntake();
    Command command = new IntakePracticeCommand(intake);
    scheduler.schedule(command);

    command.cancel();

    assertFalse(command.isScheduled());
    assertFalse(intake.isRunning());
    assertEquals(1, intake.stopCalls);
  }

  @Test
  void anotherCommandRequiringIntakeInterruptsPracticeCommand() {
    TrackingIntake intake = new TrackingIntake();
    Command practice = new IntakePracticeCommand(intake);
    Command replacement = Commands.run(() -> {}, intake);
    scheduler.schedule(practice);

    scheduler.schedule(replacement);

    assertFalse(practice.isScheduled());
    assertTrue(replacement.isScheduled());
    assertFalse(intake.isRunning());
    assertEquals(1, intake.stopCalls);
  }

  @Test
  void disablingRobotInterruptsIntakeCommand() {
    TrackingIntake intake = new TrackingIntake();
    Command command = new IntakePracticeCommand(intake);
    scheduler.schedule(command);
    DriverStationSim.setEnabled(false);
    DriverStationSim.notifyNewData();

    scheduler.run();

    assertFalse(command.isScheduled());
    assertFalse(intake.isRunning());
    assertEquals(1, intake.stopCalls);
  }

  @Test
  void emptyAutonomousCommandFinishesAfterOneSchedulerCycle() {
    RobotContainer container = new RobotContainer();
    Command autonomous = container.getAutonomousCommand();
    assertNotNull(autonomous);

    scheduler.schedule(autonomous);
    scheduler.run();

    assertFalse(autonomous.isScheduled());
  }

  /** Records command requests independently of the rookie's unfinished intake implementation. */
  private static class TrackingIntake extends IntakeSubsystem {
    private int startCalls;
    private int stopCalls;
    private boolean running;

    @Override
    public void start() {
      startCalls++;
      running = true;
    }

    @Override
    public void stop() {
      stopCalls++;
      running = false;
    }

    @Override
    public boolean isRunning() {
      return running;
    }
  }
}
