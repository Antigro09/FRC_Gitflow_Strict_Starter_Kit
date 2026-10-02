package frc.robot;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import edu.wpi.first.hal.HAL;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import edu.wpi.first.wpilibj2.command.Commands;
import frc.robot.subsystems.drive.DriveSubsystem;
import frc.robot.subsystems.intake.IntakeSubsystem;
import frc.robot.subsystems.shooter.ShooterSubsystem;
import frc.robot.subsystems.vision.VisionSubsystem;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** Verifies mode transitions and scheduler integration using hardware-free request state. */
class RobotLifecycleTest {
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
  void defaultRobotRunsCommandsAndSubsystemPeriodicThenInterruptsOnDisable() {
    TrackingIntake intake = new TrackingIntake();
    AtomicInteger executions = new AtomicInteger();
    AtomicBoolean interrupted = new AtomicBoolean();
    Command command = Commands.run(executions::incrementAndGet, intake).finallyDo(interrupted::set);

    try (Robot robot = new Robot()) {
      scheduler.schedule(command);

      robot.robotPeriodic();

      assertEquals(1, executions.get(), "robotPeriodic must execute scheduled commands");
      assertEquals(1, intake.periodicCalls, "robotPeriodic must service registered subsystems");
      assertTrue(command.isScheduled());

      robot.disabledInit();

      assertFalse(command.isScheduled());
      assertTrue(interrupted.get(), "Disabled initialization must interrupt active commands");
    }
  }

  @Test
  void autonomousStartsSelectedCommandAndTeleopCancelsOnlyThatCommand() {
    PracticeState state = new PracticeState();
    Command autonomous = Commands.startEnd(state.intake::start, state.intake::stop, state.intake);
    SelectedAutonomousContainer container = new SelectedAutonomousContainer(state, autonomous);
    AtomicInteger unrelatedExecutions = new AtomicInteger();
    Command unrelated = Commands.run(unrelatedExecutions::incrementAndGet, state.shooter);

    try (Robot robot = new Robot(container)) {
      robot.autonomousInit();
      scheduler.schedule(unrelated);

      assertEquals(1, container.selections);
      assertTrue(autonomous.isScheduled());
      assertTrue(state.intake.isRunning());
      assertEquals(1, state.intake.startCalls);

      robot.teleopInit();
      robot.robotPeriodic();

      assertFalse(autonomous.isScheduled());
      assertFalse(state.intake.isRunning());
      assertEquals(1, state.intake.stopCalls);
      assertTrue(unrelated.isScheduled(), "Teleop must preserve unrelated commands");
      assertEquals(1, unrelatedExecutions.get());
    }
  }

  @Test
  void absentAutonomousSelectionLeavesUnrelatedCommandRunningThroughTeleop() {
    PracticeState state = new PracticeState();
    SelectedAutonomousContainer container = new SelectedAutonomousContainer(state, null);
    AtomicInteger executions = new AtomicInteger();
    Command unrelated = Commands.run(executions::incrementAndGet, state.drive);

    try (Robot robot = new Robot(container)) {
      scheduler.schedule(unrelated);

      robot.autonomousInit();
      robot.teleopInit();
      robot.robotPeriodic();

      assertEquals(1, container.selections);
      assertTrue(unrelated.isScheduled());
      assertEquals(1, executions.get());
      assertEquals(0, state.intake.startCalls, "An absent autonomous must not start an intake");
      assertEquals(0, state.intake.stopCalls, "No autonomous means no teleop cancellation");
    }
  }

  @Test
  void disabledInitCancelsAllCommandsAndClearsUnownedOutputRequests() {
    PracticeState state = new PracticeState();
    RobotContainer container = state.container();
    Command intake = container.createIntakePracticeCommand();
    AtomicInteger unrelatedExecutions = new AtomicInteger();
    AtomicBoolean unrelatedInterrupted = new AtomicBoolean();
    Command unrelated =
        Commands.run(unrelatedExecutions::incrementAndGet).finallyDo(unrelatedInterrupted::set);
    state.drive.setRequestedSpeed(0.75);
    state.shooter.setTargetRpm(3500.0);

    try (Robot robot = new Robot(container)) {
      scheduler.schedule(intake, unrelated);
      robot.robotPeriodic();
      assertTrue(state.intake.isRunning());
      assertEquals(0.75, state.drive.getRequestedSpeed());
      assertEquals(3500.0, state.shooter.getTargetRpm());
      assertEquals(1, unrelatedExecutions.get());

      robot.disabledInit();

      assertFalse(intake.isScheduled());
      assertFalse(unrelated.isScheduled());
      assertTrue(unrelatedInterrupted.get());
      assertFalse(state.intake.isRunning());
      assertEquals(
          2, state.intake.stopCalls, "Cancellation and stopAll each request an intake stop");
      assertEquals(0.0, state.drive.getRequestedSpeed());
      assertEquals(
          1, state.drive.zeroRequests, "stopAll must stop a drive without an active command");
      assertEquals(0.0, state.shooter.getTargetRpm());
      assertEquals(
          1, state.shooter.zeroRequests, "stopAll must also stop an unowned shooter request");
    }
  }

  @Test
  void testInitInterruptsEveryCommandIncludingAnIntakeCommand() {
    PracticeState state = new PracticeState();
    RobotContainer container = state.container();
    Command intake = container.createIntakePracticeCommand();
    AtomicInteger executions = new AtomicInteger();
    AtomicBoolean interrupted = new AtomicBoolean();
    Command unrelated = Commands.run(executions::incrementAndGet).finallyDo(interrupted::set);

    try (Robot robot = new Robot(container)) {
      scheduler.schedule(intake, unrelated);
      robot.robotPeriodic();
      assertTrue(state.intake.isRunning());
      assertEquals(1, executions.get());

      robot.testInit();

      assertFalse(intake.isScheduled());
      assertFalse(unrelated.isScheduled());
      assertTrue(interrupted.get());
      assertFalse(state.intake.isRunning());
      assertEquals(1, state.intake.stopCalls);
    }
  }

  @Test
  void containerExposesOwnedVisionAndCreatesCommandForOwnedIntake() {
    PracticeState state = new PracticeState();
    RobotContainer container = state.container();
    Command intake = container.createIntakePracticeCommand();

    assertSame(state.vision, container.getVisionSubsystem());
    assertEquals(Set.of(state.intake), intake.getRequirements());

    scheduler.schedule(intake);
    assertTrue(state.intake.isRunning());
    assertEquals(1, state.intake.startCalls);

    intake.cancel();
    assertFalse(state.intake.isRunning());
    assertEquals(1, state.intake.stopCalls);
  }

  /** Test state is separate from, and does not complete, any rookie subsystem TODO. */
  private static class PracticeState {
    private final TrackingDrive drive = new TrackingDrive();
    private final TrackingIntake intake = new TrackingIntake();
    private final TrackingShooter shooter = new TrackingShooter();
    private final VisionSubsystem vision = new VisionSubsystem();

    private RobotContainer container() {
      return new RobotContainer(drive, intake, shooter, vision);
    }
  }

  private static class SelectedAutonomousContainer extends RobotContainer {
    private final Command autonomous;
    private int selections;

    private SelectedAutonomousContainer(PracticeState state, Command autonomous) {
      super(state.drive, state.intake, state.shooter, state.vision);
      this.autonomous = autonomous;
    }

    @Override
    public Command getAutonomousCommand() {
      selections++;
      return autonomous;
    }
  }

  private static class TrackingDrive extends DriveSubsystem {
    private double requestedSpeed;
    private int zeroRequests;

    @Override
    public void setRequestedSpeed(double speed) {
      requestedSpeed = speed;
      if (speed == 0.0) {
        zeroRequests++;
      }
    }

    @Override
    public double getRequestedSpeed() {
      return requestedSpeed;
    }
  }

  private static class TrackingShooter extends ShooterSubsystem {
    private double targetRpm;
    private int zeroRequests;

    @Override
    public void setTargetRpm(double rpm) {
      targetRpm = rpm;
      if (rpm == 0.0) {
        zeroRequests++;
      }
    }

    @Override
    public double getTargetRpm() {
      return targetRpm;
    }
  }

  private static class TrackingIntake extends IntakeSubsystem {
    private int startCalls;
    private int stopCalls;
    private int periodicCalls;
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

    @Override
    public void periodic() {
      super.periodic();
      periodicCalls++;
    }
  }
}
