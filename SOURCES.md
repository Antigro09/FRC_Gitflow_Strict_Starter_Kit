# Technical sources and pinned components

Reviewed September 24, 2026. Team-specific branch names, approval counts, coverage
thresholds and deployment policy are design choices, not requirements imposed by FRC.
Official platform/tool sources describe the mechanisms below. The kit adds the policy.

## Workflow and enforcement

- Git-flow-next (installation and commands): https://github.com/gittower/git-flow-next
- Git-flow-next init manual: https://github.com/gittower/git-flow-next/blob/main/docs/git-flow-init.1.md
- Git-flow-next configuration, topic parents/finish behavior: https://github.com/gittower/git-flow-next/blob/main/CONFIGURATION.md
- GitHub protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Ruleset REST schema: https://docs.github.com/en/rest/repos/rules
- Required status check behavior: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
- CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Merge queues: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- Actions environments, reviewer/plan limits and PR-ref restrictions: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- Actions security: https://docs.github.com/en/actions/reference/security/secure-use

## WPILib and Java checks

- Official WPILib CI; explicitly documents using the 2025 image for 2026: https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/robot-code-ci.html
- WPILib formatting guidance: https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/code-formatting.html
- Spotless 6.25.0 plugin: https://plugins.gradle.org/plugin/com.diffplug.spotless/6.25.0
- Gradle PMD: https://docs.gradle.org/current/userguide/pmd_plugin.html
- PMD 7.10.0 Java rules: https://docs.pmd-code.org/pmd-doc-7.10.0/pmd_rules_java_bestpractices.html
- PMD correctness rules: https://docs.pmd-code.org/pmd-doc-7.10.0/pmd_rules_java_errorprone.html
- Gradle JaCoCo: https://docs.gradle.org/current/userguide/jacoco_plugin.html
- Gradle wrapper verification: https://docs.gradle.org/current/userguide/gradle_wrapper.html
- Gitleaks CLI: https://github.com/gitleaks/gitleaks

## Immutable action pins and scanner download

- actions/checkout v6.1.0: d23441a48e516b6c34aea4fa41551a30e30af803
  https://github.com/actions/checkout/commit/d23441a48e516b6c34aea4fa41551a30e30af803
- actions/upload-artifact v7.0.1: 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
  https://github.com/actions/upload-artifact/commit/043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
- gradle/actions wrapper-validation v6.3.0: 9c971963bec38e04b3d30dcc455b5382be2fdbfb
  https://github.com/gradle/actions/commit/9c971963bec38e04b3d30dcc455b5382be2fdbfb
- Gitleaks v8.30.1 Linux x64 archive:
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
  SHA256: 551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
  Official release/assets: https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1

These are explicit reviewed pins, not a promise that they remain the latest or free of
future vulnerabilities. Update versions/checksums deliberately with review. The WPILib
image uses an official version tag, not a digest; verify and pin its pulled digest for
stronger immutability. None of these source checks substitutes for running the kit
against the actual robot project and GitHub account configuration.

## Java command robot added October 2, 2026

The project uses the stable **2026.2.1 WPILib VS Code template**, Java 17, and
Gradle 8.11. These upstream files were retrieved from versioned official sources:

- GradleRIO/build/editor/wrapper templates: https://github.com/wpilibsuite/vscode-wpilib/tree/v2026.2.1/vscode-wpilib/resources/gradle
- Main/Robot command template (adapted package and disabled cleanup): https://github.com/wpilibsuite/allwpilib/tree/v2026.2.1/wpilibjExamples/src/main/java/edu/wpi/first/wpilibj/templates/commandbased
- Command-library vendordep: https://github.com/wpilibsuite/allwpilib/blob/v2026.2.1/wpilibNewCommands/WPILibNewCommands.json
- Project structure: https://docs.wpilib.org/en/stable/docs/software/commandbased/structuring-command-based-project.html
- Annotation library coordinates (`org.wpilib:annotations-java:2026.2.1`): https://github.com/wpilibsuite/allwpilib/blob/v2026.2.1/wpiannotations/build.gradle

The annotation library is explicitly on the production/test compile-only classpaths
so the existing strict `-Xlint:all -Werror` compiler can resolve WPILib's `NoDiscard`
class-file annotations. A group-limited repository uses WPILib's official Maven
release download endpoint to resolve `org.wpilib` artifacts. WPILib's annotation processor remains configured separately.

The wrapper JAR SHA256 was matched to Gradle's official checksum:
`2db75c40782f5e8ba1fc278a5574bab070adccb2d21ca5a6e5ed840888448046`
(https://services.gradle.org/distributions/gradle-8.11-wrapper.jar.sha256).
The distribution checksum is pinned in `gradle-wrapper.properties`:
`57dafb5c2622c6cc08b993c85b7c06956a2f53536432a30ead46166dbca0f1e9`
(https://services.gradle.org/distributions/gradle-8.11-bin.zip.sha256).
`WPILib-License.md` is included unchanged from the official template.
