module com.beginsecure.hellofx {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;

    opens com.beginsecure.hellofx to javafx.fxml;
    exports com.beginsecure.hellofx;
}