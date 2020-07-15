use std::io;
use std::io::Write;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    let secret_guess = rand::thread_rng().gen_range(0, 101);
    let mut guess_input = String::new();
    let mut try_count = 0;

    println!("Guess the correct number between 1-100.");

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

        let guess: i32 = match guess_input.trim().parse() {
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
