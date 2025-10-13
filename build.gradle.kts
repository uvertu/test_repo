plugins {
    java
    application
    id("org.javamodularity.moduleplugin") version "1.8.15"
    id("org.openjfx.javafxplugin") version "0.0.13"
    id("org.beryx.jlink") version "2.25.0"
    checkstyle
}

group = "com.beginsecure"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

val junitVersion = "5.12.1"

checkstyle {
    toolVersion = "10.12.4"
    configFile = file("${rootDir}/config/checkstyle/checkstyle.xml")
}

tasks.withType<Checkstyle>().configureEach {
    reports {
        xml.required.set(false)
        html.required.set(true)
    }
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(22)
    }
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
}

application {
    mainModule.set("com.beginsecure.hellofx")
    mainClass.set("com.beginsecure.hellofx.HelloApplication")
}

javafx {
    version = "22.0.1"
    modules = listOf("javafx.controls", "javafx.fxml")
}

dependencies {
    implementation("org.controlsfx:controlsfx:11.2.1")
    testImplementation("org.junit.jupiter:junit-jupiter-api:${junitVersion}")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:${junitVersion}")
}

tasks.withType<Test> {
    useJUnitPlatform()
}

jlink {
    imageZip.set(layout.buildDirectory.file("/distributions/app-${javafx.platform.classifier}.zip"))
    options.set(listOf("--strip-debug", "--compress", "2", "--no-header-files", "--no-man-pages"))
    launcher {
        name = "app"
    }
}
