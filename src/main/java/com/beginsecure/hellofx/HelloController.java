package com.beginsecure.hellofx;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.control.ListView;

public class HelloController {
    private int targetNumber = (int) (Math.random() * 100) + 1;
    private int attempts = 0;
    private int minRange = 1;
    private int maxRange = 100;

    @FXML
    private Label infoLabel;

    @FXML
    private Label rangeLabel;

    @FXML
    private TextField guessField;

    @FXML
    private ListView<String> historyList;

    @FXML
    protected void onGuessAction() {
        try {
            int guess = Integer.parseInt(guessField.getText());
            if (guess < minRange || guess > maxRange) {
                infoLabel.setText("Введите число " + minRange + "-" + maxRange + "!");
                return;
            }

            attempts++;
            historyList.getItems().add("Попытка " + attempts + ": " + guess);

            if (guess < targetNumber) {
                infoLabel.setText("Больше! Попыток: " + attempts);
                minRange = guess + 1;
            } else if (guess > targetNumber) {
                infoLabel.setText("Меньше! Попыток: " + attempts);
                maxRange = guess - 1;
            } else {
                infoLabel.setText("Верно! Попытка: " + attempts + ". Новая игра началась.");
                resetGame();
            }
            updateRangeLabel();
            guessField.clear();
        } catch (NumberFormatException e) {
            infoLabel.setText("Введите корректное число!");
        }
    }

    @FXML
    protected void onNewGame() {
        resetGame();
        infoLabel.setText("Новая игра началась! Угадай число 1-100");
        historyList.getItems().clear();
        updateRangeLabel();
    }

    private void updateRangeLabel() {
        rangeLabel.setText("Интервал: " + minRange + "-" + maxRange);
    }

    private void resetGame() {
        targetNumber = (int) (Math.random() * 100) + 1;
        attempts = 0;
        minRange = 1;
        maxRange = 100;
    }
}