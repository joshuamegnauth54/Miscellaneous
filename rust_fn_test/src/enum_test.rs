#[derive(Copy, Clone)]
pub enum Pokemans {
    Pikachu = 25,
    Vaporeon = 134,
    Jolteon = 135,
    Flareon = 136,
    Mew = 151,
    Espeon = 196,
    Umbreon = 197,
    Girafarig = 203,
    Skitty = 300,
    Delcatty = 301,
    Drampa = 780,
}

impl Pokemans {
    pub fn is_best(&self) -> bool {
        true
    }

    pub fn is_kitty(&self) -> bool {
        match self {
            Pokemans::Mew | Pokemans::Espeon | Pokemans::Skitty | Pokemans::Delcatty => true,
            _ => false,
        }
    }

    pub fn is_giraffe(&self) -> bool {
        match self {
            Pokemans::Girafarig => true,
            _ => false,
        }
    }

    pub fn generation(&self) -> u32 {
        match *self as u32 {
            0..=151 => 1,
            152..=251 => 2,
            252..=386 => 3,
            387..=493 => 4,
            494..=649 => 5,
            650..=721 => 6,
            722..=810 => 7,
            _ => 8,
        }
    }
}
