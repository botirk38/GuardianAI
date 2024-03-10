// Bad code

// Vulnerability: UnsafeBlock (0101)
unsafe {
    let ptr: *const i32 = 1 as *const i32; // Improper use of raw pointers
    println!("{}", *ptr); // Dereferencing a raw pointer without ensuring it points to valid memory
}

// Vulnerability: EnumVariant (0100)
// This example itself might not directly illustrate a vulnerability but follows the mapping provided.
enum MyEnum {
    EnumVariant(LargeData), // Potential for misuse if LargeData is not properly handled
}

struct LargeData {
    data: Vec<u8>, // Hypothetical large data container
}

impl LargeData {
    fn new(size: usize) -> Self {
        LargeData { data: vec![0; size] } // Potentially allocating a large amount of memory unsafely
    }
}

// Additional Vulnerability: StaticMut (0011)
static mut GLOBAL_STATE: i32 = 0; // Unsafe use of mutable statics can lead to data races

fn main() {
    unsafe {
        GLOBAL_STATE = 42; // Modification without synchronization
    }
}



// Good code

// Safe handling of potentially large data without relying on raw enum variants directly
struct SafeLargeData {
    data: Vec<u8>,
}

impl SafeLargeData {
    fn new(size: usize) -> Self {
        if size > 1024 {
            panic!("Requesting too much data"); // Safeguard against excessively large allocations
        } else {
            SafeLargeData { data: vec![0; size] } // Controlled allocation
        }
    }
}

// Using safe constructs and avoiding unsafe blocks when not necessary
fn print_number(num: i32) {
    println!("{}", num); // Safe operations within Rust's safety guarantees
}

fn main() {
    let safe_data = SafeLargeData::new(512); // Safe usage example
    print_number(42); // Safe function call
}


// Mid Example: Using an unsafe block cautiously
fn get_data_from_raw_pointer() -> i32 {
    let data: i32 = 10; // Simulated data source
    let ptr: *const i32 = &data; // Safe conversion to raw pointer
    unsafe {
        // Cautiously dereferencing a raw pointer within an unsafe block
        // Ensuring the pointer is not null and points to valid data
        if !ptr.is_null() {
            *ptr
        } else {
            0 // Default value if pointer is null (safety measure)
        }
    }
}

// Mid Example: Enum with variant holding a wrapper around potentially large data
enum DataHolder {
    LargeDataWrapper(SafeWrapper),
}

// A wrapper struct that aims to provide safer access to potentially large data
struct SafeWrapper {
    data: Vec<u8>, // Encapsulated data
}

impl SafeWrapper {
    // Constructor function that includes a basic size check
    fn new(size: usize) -> Option<Self> {
        if size <= 1024 { // Limiting size to avoid excessive allocation
            Some(SafeWrapper { data: vec![0; size] })
        } else {
            None // Returning None if requested size is too large
        }
    }
}

// Usage of a static mutable variable with an attempt at minimizing risk
static mut COUNTER: i32 = 0;

fn increment_counter_safely() {
    unsafe {
        // Accessing and modifying the static mutable variable within an unsafe block
        // This pattern remains risky due to potential data races in a multi-threaded context
        COUNTER += 1;
        println!("COUNTER: {}", COUNTER);
    }
}

fn main() {
    let num = get_data_from_raw_pointer();
    println!("Number from raw pointer: {}", num);

    if let Some(wrapper) = SafeWrapper::new(512) {
        println!("Successfully created SafeWrapper with size 512");
    } else {
        println!("Failed to create SafeWrapper due to size limit");
    }

    increment_counter_safely(); // Incrementing a counter with a simplistic safety attempt
}

