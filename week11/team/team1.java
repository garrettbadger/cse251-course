/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1

Instructions:

- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.

- DON'T copy/slice the array in main() for each thread.

Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.

************************************/
import java.util.Random; 
import java.lang.Math; 

class Main {

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }

  public static void main(String[] args) {
    System.out.println("Hello world!");

    // create instance of Random class 
    Random rand = new Random(); 

    int count = 1000;
    int[] array = new int[count];
    for (int i = 0; i < count; i++) 
    {
      array[i] = Math.abs(rand.nextInt());
    }
    int threadCount = 4;
    int chunkSize = count / threadCount;
    int startIndex = 0;
    int endIndex = chunkSize -1;
    MyThread[] threads = new MyThread[threadCount];
    for (int i = 0; i < numThreads; i++) {
      if (i == numThreads - 1) {
          endIndex = count - 1; // Adjust the endIndex for the last thread
      }
      threads[i] = new PrimeThread(array, startIndex, endIndex);
      threads[i].start();

      startIndex = endIndex + 1;
      endIndex += chunkSize;
  }

  // TODO - this is just sample code. you can remove it.
  for (int i = 0; i < numThreads; i++) {
    try {
        threads[i].join();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
  }
  }
}
class MyThread extends Thread {  

    private int startIndex;
    private int endIndex;
    private int[] array;

    public MyThread(int startIndex, int endIndex, int[] array){
      this.array = array;
      this.startIndex = startIndex;
      this.endIndex = endIndex;
    }
  @Override
  public void run() {  
      for (int i = startIndex; i <= int endIndex; i++){
        if (isPrime(array[i])){
          System.out.println("thread is running..." + Thread.currentThread().getId());
        }
        
      }
        
  }

}

