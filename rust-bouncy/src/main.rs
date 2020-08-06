use pancurses::{endwin, initscr, noecho, Input, Window};

enum VertDir {
    Up,
    Down,
}

enum HorizDir {
    Left,
    Right,
}

struct Ball {
    x: i32,
    y: i32,
    vert_dir: VertDir,
    horiz_dir: HorizDir,
}

struct Frame {
    window: Window,
}

struct Game {
    frame: Frame,
    ball: Ball,
}

impl Game {
    fn new(sleep_duration: i32) -> Game {
        Game {
            frame: Frame::new(sleep_duration),
            ball: Ball {
                x: 2,
                y: 4,
                vert_dir: VertDir::Up,
                horiz_dir: HorizDir::Left,
            },
        }
    }

    fn step(&mut self) {
        self.ball.bounce(&self.frame);
        self.ball.mv();
    }

    fn game_loop(&mut self) {
        while self.frame.handle_quit_input() {
            self.frame.reset();
            self.frame.draw_border();
            self.frame.draw_ball(&mut self.ball);
            self.frame.update();
            self.step();
        }
    }
}

impl Ball {
    fn bounce(&mut self, frame: &Frame) {
        if self.x == 0 {
            self.horiz_dir = HorizDir::Right;
        } else if self.x == frame.width() {
            self.horiz_dir = HorizDir::Left;
        }

        if self.y == 0 {
            self.vert_dir = VertDir::Down;
        } else if self.y == frame.height() {
            self.vert_dir = VertDir::Up;
        }
    }

    fn mv(&mut self) {
        match self.horiz_dir {
            HorizDir::Left => self.x -= 1,
            HorizDir::Right => self.x += 1,
        }
        match self.vert_dir {
            VertDir::Up => self.y -= 1,
            VertDir::Down => self.y += 1,
        }
    }
}

impl Frame {
    fn new(sleep_duration: i32) -> Frame {
        let window = initscr();
        window.timeout(sleep_duration);
        Frame { window }
    }

    fn height(&self) -> i32 {
        self.window.get_max_y() - 1
    }

    fn width(&self) -> i32 {
        self.window.get_max_x() - 1
    }

    fn reset(&self) {
        self.window.clear();
    }

    fn draw_border(&self) {
        self.window.border('|', '|', '-', '-', '+', '+', '+', '+');
    }

    fn draw_ball(&self, ball: &Ball) {
        self.window.mv(ball.y as i32, ball.x as i32);
        self.window.addch('o');
    }

    fn update(&self) {
        self.window.refresh();
    }

    fn handle_quit_input(&self) -> bool {
        // Returns false on q.
        match self.window.getch() {
            Some(Input::Character(c)) => match c {
                'q' => false,
                _ => true,
            },
            _ => true,
        }
    }
}

impl Drop for Frame {
    fn drop(&mut self) {
        endwin();
    }
}

fn main() {
    let mut game = Game::new(33);
    game.game_loop();
}
