% Define parameters
L1 = 50; % Length of the first arm segment
L2 = 40; % Length of the second arm segment

% Define fish shape as (x, y) coordinates including a tail triangle.
% The fish body starts at the tail base (0,0) and goes to the head at (25,0).
% The tail triangle is drawn before the body using points (-5,5) and (-5,-5).
fish_points = [
    15, 0;      % Tail base (also used to join tail and body)
    10, 5;     % Tail triangle top
    10, -5;    % Tail triangle bottom
    15, 0;      % Tail base again to complete the tail triangle
    20, 5;      % Upper body points begin
    25, 10;
    30, 7;
    35, 3;
    40, 0;     % Head of the fish
    35, -3;
    30, -7;
    25, -10;
    20, -5;
    15, 0;      % Close the fish shape (back to tail base)
];

% Initialize figure
figure;
axis equal;
axis([-60 60 -60 60]); % Adjust axis limits to fit the drawing
hold on;
grid on;

% Plot the fish outline for reference
plot(fish_points(:, 1), fish_points(:, 2), '--k', 'LineWidth', 1.5); % Fish outline
scatter(fish_points(:, 1), fish_points(:, 2), 'filled', ...
    'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'g'); % Fish points
title('Robotic Arm Drawing a Fish');
xlabel('X-axis');
ylabel('Y-axis');

% Loop through each point on the fish
for i = 1:size(fish_points, 1)
    % Target end-effector position
    x = fish_points(i, 1);
    y = fish_points(i, 2);

    % Calculate the distance to the target point
    distance = sqrt(x^2 + y^2);

    % Clamp the distance to be within the workspace
    if distance > (L1 + L2)
        distance = L1 + L2; % Maximum reach
    elseif distance < abs(L1 - L2)
        distance = abs(L1 - L2); % Minimum reach
    end

    % Scale x and y to the clamped distance
    if distance > 0
        scale = distance / sqrt(x^2 + y^2);
        x = x * scale;
        y = y * scale;
    end

    % Inverse Kinematics calculations
    cos_theta2 = (x^2 + y^2 - L1^2 - L2^2) / (2 * L1 * L2);
    theta2 = acos(cos_theta2); % Elbow angle
    theta1 = atan2(y, x) - atan2(L2 * sin(theta2), L1 + L2 * cos(theta2)); % Shoulder angle

    % Joint positions
    X1 = L1 * cos(theta1);
    Y1 = L1 * sin(theta1);
    X2 = X1 + L2 * cos(theta1 + theta2);
    Y2 = Y1 + L2 * sin(theta1 + theta2);

    % Plot the robotic arm
    plot([0, X1, X2], [0, Y1, Y2], '-o', 'LineWidth', 2, 'MarkerSize', 8, ...
        'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'k'); % Arm
    hold on;

    % Highlight the current target point
    scatter(x, y, 80, 'r', 'filled'); % Current target

    % Pause for animation effect
    pause(0.3);

    % Clear the arm for the next iteration (but keep the fish outline)
    if i < size(fish_points, 1)
        cla; % Clear axes to redraw
        plot(fish_points(:, 1), fish_points(:, 2), '--k', 'LineWidth', 1.5); % Replot fish shape
        scatter(fish_points(:, 1), fish_points(:, 2), 'filled', ...
            'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'g'); % Replot fish points
    end
end

disp('Fish drawing complete!');
