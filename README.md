# ColorCatcher

ColorCatcher is a user-friendly tool designed to extract and display dominant colors from images. It's perfect for designers, artists, and anyone interested in color analysis.

## Features

- Extract dominant colors from any image.
- Display color palette with both RGB and HEX codes.
- Interactive GUI for easy operation.
- Customize the number of colors to extract.

## Installation

To use ColorCatcher, follow these simple installation steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/slash-se/ColorCatcher.git
   cd ColorCatcher
2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt

## Usage

1. **Run ColorCatcher**:
   ```sh
   python ColorCatcher.py

2. **Select Number of Colors**: Use the spinbox in the GUI to set the desired number of colors to extract.

3. **Choose an Image**: Click the '...' button to select an image file.

4. **Process the Image**: Click 'Process' to extract the color palette.

5. **View Results**: The original image and its color palette will be displayed. Click on any color in the palette to copy its RGB or HEX value.

6. **Select Another Image**: Process another image without restarting the application.

## Configuration

- Adjust the default number of colors in the `config.ini` file.
- The configuration file can be found in the application's root directory.

## Builds

Standalone executables for Windows, macOS, and Linux are available in the [Releases](https://github.com/slash-se/ColorCatcher/releases) section.

### Downloading and Running Builds

1. Navigate to [Releases](https://github.com/slash-se/ColorCatcher/releases).
2. Download the appropriate executable for your operating system.
3. Run the downloaded file to start ColorCatcher.

## Contributing

Contributions to ColorCatcher are welcome! Please refer to the [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

ColorCatcher is released under the [GNU General Public License v3.0](LICENSE).
