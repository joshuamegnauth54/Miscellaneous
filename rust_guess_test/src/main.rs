use std::io;
use std::io::Write;
use std::cmp::Ordering;
use rand::Rng;

const MIN_GUESS: i16 = 0;
const MAX_GUESS: i16 = 101;

fn main() {
    let secret_guess: i16 = rand::thread_rng().gen_range(MIN_GUESS, MAX_GUESS);
    let mut guess_input = String::new();
    let mut try_count = 0;

    println!("Guess the correct number between {}-{}.",
        MIN_GUESS, MAX_GUESS);

    loop {
        try_count = try_count + 1;
        print!("Guess: ");
        io::stdout()
            .flush()
            .expect("Failed to write to stdout.");

        guess_input.clear();
        io::stdin()
            .read_line(&mut guess_input)
            .expect("Failed to read from stdin.");

        let guess: i16 = match guess_input.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                eprintln!("Numbers only.");
                continue;
            }
        };

        match guess.cmp(&secret_guess) {
            Ordering::Less => println!("Too low!"),
            Ordering::Greater => println!("Too high!"),
            Ordering::Equal => {
                println!("Just right!");
                break;
           }
        }
    }

    println!("Required guess[es]: {}", try_count);
}
