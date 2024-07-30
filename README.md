# RPiModules

## Description

RPiModules is a versatile platform for managing and controlling various modules on your Raspberry Pi (RPi). It provides a web interface for easy configuration and monitoring of the installed modules. RPiModules is designed to be modular, allowing you to add custom modules to enhance its functionality.

## Installation

1. Clone the RPiModules repository to your RPi.

   ```
   git clone https://github.com/Vasysik/RPiModules.git /path/to/RPiModules
   ```

2. Install the RPiModules service.

   ```
   sudo cp /path/to/RPiModules/rpi_modules.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable rpi_modules.service
   sudo systemctl start rpi_modules.service
   ```

3. Access the RPiModules web interface by navigating to `http://your_rpi_ip:5000` in your web browser.

## Usage

RPiModules provides a web interface for easy configuration and monitoring of the installed modules. You can add custom modules to enhance its functionality. The repository includes a sample module for testing purposes.

## Adding Custom Modules

To add a custom module to RPiModules, follow these steps:

1. Create a new directory for your module within the `modules` directory of your RPiModules installation.

   ```
   mkdir /path/to/RPiModules/modules/my_module
   ```

2. Implement your module's functionality in the `my_module` directory.

3. Open the `modules.json` file located in your RPiModules directory and add the following configuration for your module:

   ```json
   "my_module": {
       "route": "my_module",
       "icon": "my_module/static/my_module_icon.png",
       "name": "My Module",
       "enable": true
   }
   ```

4. Restart the RPiModules service to load your new module.

   ```
   sudo systemctl restart rpi_modules.service
   ```

5. Access your new module through the RPiModules web interface.

## Sample Module

The RPiModules repository includes a sample module for testing purposes. The sample module can be found in the `modules/sample` directory. You can use this module as a starting point for creating your own custom modules.

## Contributing

Contributions to RPiModules are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository. Pull requests are also encouraged.
