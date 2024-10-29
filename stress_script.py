import psutil
import subprocess
import time
import mysql.connector
import logging

# Configure logging
logging.basicConfig(
    filename='stress_test.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class StressTest:
    def __init__(self):
        self.mysql_config = {
            'host': '192.168.52.112',
            'user': 'stress',
            'password': 'Abc@1234',
            'database': 'stress_test_db'
        }

    def memory_stress_test(self):
        logging.info("Starting Memory Stress Test")
        try:
            # Start stress-ng for memory testing
            subprocess.Popen(["stress-ng", "--vm", "2", "--vm-bytes", "80%", "--timeout", "60s"])
            
            memory_usage = psutil.virtual_memory().percent
            logging.info(f"Memory Usage: {memory_usage}%")
        except Exception as e:
            logging.error(f"Memory stress test error: {str(e)}")

    def disk_stress_test(self):
        logging.info("Starting Disk Stress Test")
        try:
            # Start stress-ng for disk testing
            subprocess.Popen(["stress-ng", "--io", "4", "--timeout", "60s"])
            
            disk_usage = psutil.disk_usage('/').percent
            logging.info(f"Disk Usage: {disk_usage}%")
        except Exception as e:
            logging.error(f"Disk stress test error: {str(e)}")

    def network_stress_test(self):
        logging.info("Starting Network Stress Test")
        try:
            # Start iperf3 server on vm_2
            subprocess.Popen(["iperf3", "-c", "vm2", "-t", "60", "-p", "5201"])
            
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent / 1024 / 1024
            bytes_recv = net_io.bytes_recv / 1024 / 1024
            logging.info(f"Network I/O - Sent: {bytes_sent} MB, Received: {bytes_recv} MB")
            
            # Calculate network usage (simplified)
            network_usage = (bytes_sent + bytes_recv) / 100
        except Exception as e:
            logging.error(f"Network stress test error: {str(e)}")

    def cpu_stress_test(self):
        logging.info("Starting CPU Stress Test")
        try:
            # Start stress-ng for CPU testing
            subprocess.Popen(["stress-ng", "--cpu", "4", "--timeout", "60s"])
            
            cpu_usage = psutil.cpu_percent()
            logging.info(f"CPU Usage: {cpu_usage}%")
        except Exception as e:
            logging.error(f"CPU stress test error: {str(e)}")

    def mysql_stress_test_old(self):
        logging.info("Starting MySQL Stress Test")
        try:
            # Run sysbench for MySQL stress testing
            command = (
                f"sysbench --db-driver=mysql --mysql-host={self.mysql_config['host']} "
                f"--mysql-user={self.mysql_config['user']} --mysql-password={self.mysql_config['password']} "
                f"--mysql-db={self.mysql_config['database']} oltp_read_only --table-size=1000 --threads=4 --time=60 run"
            )
            
            # Execute the sysbench command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Check MySQL CPU usage
            mysql_cpu_usage = psutil.cpu_percent(interval=1)

            # Log the output of sysbench
            logging.info(stdout.decode())
            if stderr:
                logging.error(stderr.decode())

        except Exception as e:
            logging.error(f"MySQL stress test error: {str(e)}")

    def mysql_stress_test(self):
        logging.info("Starting MySQL Stress Test")
        try:
            connection = mysql.connector.connect(
                host=self.mysql_config['host'],
                database=self.mysql_config['database'],
                user=self.mysql_config['user'],
                password=self.mysql_config['password']
            )
            cursor = connection.cursor()
            
            # Start time and query count
            start_time = time.time()
            query_count = 0
            duration = 60  # Duration for stress test in seconds
            
            while time.time() - start_time < duration:
                cursor.execute("SELECT * FROM sbtest1 LIMIT 1")  # Example query to simulate load
                cursor.fetchall()  # Fetch all results to clear the unread result issue
                query_count += 1
            
            elapsed_time = time.time() - start_time
            qps = query_count / elapsed_time
            logging.info(f"MySQL QPS stress test completed. Approximate QPS: {qps:.2f}")
            
        except Error as e:
            logging.error("Error during MySQL QPS stress test:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def main():
    stress_tester = StressTest()

    while True:
        print("\nStress Testing Menu:")
        print("1. Memory Stress Test")
        print("2. Disk Stress Test")
        print("3. Network Stress Test")
        print("4. CPU Stress Test")
        print("5. MySQL Stress Test")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            stress_tester.memory_stress_test()
        elif choice == '2':
            stress_tester.disk_stress_test()
        elif choice == '3':
            stress_tester.network_stress_test()
        elif choice == '4':
            stress_tester.cpu_stress_test()
        elif choice == '5':
            stress_tester.mysql_stress_test()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
