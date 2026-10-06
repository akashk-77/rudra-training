#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>

const int GRID_SIZE = 20;

enum RoverState {
    IDLE,
    MOVING,
    AVOID,
    SUCCESS
};

struct Point {
    int x;
    int y;

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

class GridRover {
private:
    RoverState current_state;
    Point position;
    Point start_pos;
    Point target_pos;
    
    bool map[GRID_SIZE][GRID_SIZE];

    float linear_velocity;  // m/s
    float angular_velocity; // rad/s

public:
    GridRover(Point start, Point target) : start_pos(start), target_pos(target) {
        position = start_pos;
        current_state = IDLE;
        linear_velocity = 0.0f;
        angular_velocity = 0.0f;

        for (int i = 0; i < GRID_SIZE; ++i) {
            for (int j = 0; j < GRID_SIZE; ++j) {
                map[i][j] = false;
            }
        }
    }

    void setObstacle(int x, int y) {
        if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE) {
            map[x][y] = true;
        }
    }

    bool isObstacle(int x, int y) const {
        if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) return true;
        return map[x][y];
    }

    std::string getStateString() const {
        switch (current_state) {
            case IDLE:    return "IDLE";
            case MOVING:  return "MOVING";
            case AVOID:   return "AVOID";
            case SUCCESS: return "SUCCESS";
            default:      return "UNKNOWN";
        }
    }

    void transitionTo(RoverState newState) {
        current_state = newState;

        if (current_state == IDLE) {
            linear_velocity = 0.0f;
            angular_velocity = 0.0f;
        }
        else if (current_state == MOVING) {
            linear_velocity = 1.0f;
            angular_velocity = 0.0f;
        }
        else if (current_state == AVOID) {
            linear_velocity = 0.2f;
            angular_velocity = 0.5f;
        }
        else if (current_state == SUCCESS) {
            linear_velocity = 0.0f;
            angular_velocity = 0.0f;
        }
    }

    void update() {
        printGrid();

        if (current_state == IDLE) {
            std::cout << "[ACTION] Starting path execution from Point A...\n";
            transitionTo(MOVING);
            return;
        }

        if (current_state == SUCCESS) {
            return;
        }

        // Check if destination is reached
        if (position == target_pos) {
            transitionTo(SUCCESS);
            return;
        }

        // Calculate next intended step toward Target B
        int step_x = position.x;
        int step_y = position.y;

        if (step_x < target_pos.x) step_x++;
        else if (step_x > target_pos.x) step_x--;

        if (step_y < target_pos.y) step_y++;
        else if (step_y > target_pos.y) step_y--;

        // Check if intended step hits an obstacle
        if (isObstacle(step_x, step_y)) {
            // Trigger AVOID state
            if (current_state != AVOID) {
                transitionTo(AVOID);
            }

            // Avoidance logic: Sidestep vertically (Y-axis) or horizontally (X-axis)
            if (!isObstacle(position.x, position.y + 1) && position.y + 1 < GRID_SIZE) {
                position.y++; // Dodge down/up
            } else if (!isObstacle(position.x + 1, position.y) && position.x + 1 < GRID_SIZE) {
                position.x++; // Side step right
            } else if (!isObstacle(position.x, position.y - 1) && position.y - 1 >= 0) {
                position.y--;
            }
        } 
        else {
            // Path is clear
            if (current_state == AVOID) {
                std::cout << "[INFO] Obstacle bypassed! Returning to MOVING state.\n";
                transitionTo(MOVING);
            }
            position.x = step_x;
            position.y = step_y;
        }
    }

    void printGrid() const {
        std::cout << "\n=========================================\n";
        std::cout << " CURRENT STATE: [ " << getStateString() << " ]\n";
        std::cout << " Linear Velocity: " << linear_velocity << " m/s | Angular Velocity: " << angular_velocity << " rad/s\n";
        std::cout << " Position: (" << position.x << ", " << position.y << ")\n";
        std::cout << "=========================================\n";

        for (int y = 0; y < GRID_SIZE; ++y) {
            for (int x = 0; x < GRID_SIZE; ++x) {
                if (x == position.x && y == position.y) {
                    std::cout << "R ";
                } else if (x == target_pos.x && y == target_pos.y) {
                    std::cout << "B ";
                } else if (map[x][y]) {
                    std::cout << "X ";
                } else {
                    std::cout << ". ";
                }
            }
            std::cout << "\n";
        }
    }

    RoverState getState() const { return current_state; }
};

int main() {
    Point pointA = {0, 0};
    Point pointB = {10, 10};

    GridRover rover(pointA, pointB);

    // Place obstacles right along the direct diagonal path
    rover.setObstacle(3, 3);
    rover.setObstacle(4, 4);
    rover.setObstacle(5, 5);

    while (rover.getState() != SUCCESS) {
        rover.update();
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    // Final call to show SUCCESS state
    rover.update();

    return 0;
}
