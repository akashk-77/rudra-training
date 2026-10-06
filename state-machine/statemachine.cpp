#include <iostream>


enum RoverState {
    IDLE,
    MOVING,
    AVOID
};

class Rover {
private:
    RoverState state;
    float linear_velocity;  
    float angular_velocity; 
public:
    Rover() {
        setIdle();
    }

    void setIdle() {
        state = IDLE;
        linear_velocity = 0.0f;  
        angular_velocity = 0.0f;  
        std::cout << "[STATE] IDLE   | Linear Speed: " << linear_velocity 
                  << " m/s, Turning Speed: " << angular_velocity << " rad/s\n";
    }

    void setMoving() {
        state = MOVING;
        linear_velocity = 1.5f;  
        angular_velocity = 0.0f; 
        std::cout << "[STATE] MOVING | Linear Speed: " << linear_velocity 
                  << " m/s, Turning Speed: " << angular_velocity << " rad/s\n";
    }

    void setAvoid() {
        state = AVOID;
        linear_velocity = 0.2f;  
        angular_velocity = 0.8f;  
        std::cout << "[STATE] AVOID  | Linear Speed: " << linear_velocity 
                  << " m/s, Turning Speed: " << angular_velocity << " rad/s\n";
    }

    void updateState(RoverState newState) {
        if (newState == IDLE) {
            setIdle();
        } else if (newState == MOVING) {
            setMoving();
        } else if (newState == AVOID) {
            setAvoid();
        }
    }
};

int main() {
    Rover rover;

    std::cout << "\n--- Simulation ---\n";
    rover.updateState(MOVING); // Start moving forward
    rover.updateState(AVOID);  // Obstacle detected, slow down & turn
    rover.updateState(MOVING); // Path cleared, back to normal speed
    rover.updateState(IDLE);   

    return 0;
}
