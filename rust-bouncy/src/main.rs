use pancurses::Window;
use std::fmt::{Display, Formatter};

enum VertDir {
    Up,
    Down,
}

enum HorizDir {
    Left,
    Right,
}

struct Ball {
    x: u32,
    y: u32,
    vert_dir: VertDir,
    horiz_dir: HorizDir,
}

struct Frame {
    width: u32,
    height: u32,
}

struct Game {
    frame: Frame,
    ball: Ball,
}

impl Game {
    fn new(frame: Frame) -> Game {
        Game {
            frame,
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
}

impl Ball {
    fn bounce(&mut self, frame: &Frame) {
        if self.x == 0 {
            self.horiz_dir = HorizDir::Right;
        } else if self.x == frame.width - 1 {
            self.horiz_dir = HorizDir::Left;
        }

        if self.y == 0 {
            self.vert_dir = VertDir::Down;
        } else if self.y == frame.height - 1 {
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

impl Display for Game {
    fn fmt(&self, fmt: &mut Formatter) -> std::fmt::Result {
        let top_bottom = |fmt: &mut Formatter| {
            write!(fmt, "+")?;
            for _ in 0..self.frame.width {
                write!(fmt, "-")?;
            }
            write!(fmt, "+\n")
        };

        top_bottom(fmt)?;

        for row in 0..self.frame.height {
            write!(fmt, "|")?;

            for column in 0..self.frame.width {
                let c = if row == self.ball.y && column == self.ball.x {
                    'o'
                } else {
                    ' '
                };
                write!(fmt, "{}", c)?;
            }

            write!(fmt, "|\n")?;
        }

        top_bottom(fmt)
    }
}

impl Game {
    fn draw_border(&self, window: &pancurses::Window) {
        let vlen = self.frame.height as i32 - 1;
        let hlen = self.frame.width as i32 - 1;

        window.mv(0, 1);
        window.addch('+');
        window.hline('-', hlen);
        window.mv(0, 1);
        window.vline('|', vlen);
        window.mv(0, hlen);
        window.addch('+');
        window.vline('|', vlen);
        window.mv(vlen, 1);
        window.addch('+');
        window.hline('-', hlen);
        window.mv(vlen, hlen);
        window.addch('+');
    }

    fn draw_ball(&self, window: &pancurses::Window) {
        window.mv(self.ball.y as i32, self.ball.x as i32);
        window.addch('o');
    }
}

fn main() {
    let window = pancurses::initscr();
    let (max_y, max_x) = window.get_max_yx();
    let mut game = Game::new(Frame {
        height: max_y as u32 - 1,
        width: max_x as u32 - 1,
    });

    let sleep_duration = std::time::Duration::from_millis(33);
    loop {
        window.clear();
        game.draw_border(&window);
        game.draw_ball(&window);
        window.refresh();
        game.step();
        std::thread::sleep(sleep_duration);
    }
}
