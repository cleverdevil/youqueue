# YouQueue

An extremely simple web service for downloading videos from any website
supported by [YouTube-DL](http://ytdl-org.github.io/youtube-dl/) and dropping
them into a target directory. I personally use YouQueue to quickly grab
interesting videos and add them to my [Plex](http://plex.tv) server.

## Installation

YouQueue requires Python 3.6 or greater and a version of YouTube-DL installed
and available on your `PATH`. I personally run YouQueue on my Synology NAS as a
scheduled task. There are no external libraries or dependencies to keep things
simple.

Because YouQueue is really just a very simple script, I've not spent any time
making a complex configuration system. You'll simply want to edit the
`youqueue.py` file to set the desired `HOST` and `PORT` along with a
`DOWNLOAD_PATH`. You can also customize the filename using the `DOWNLOAD_TMPL`
variable. Refer to the [YouTube-DL Documentation](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template).

To run YouQueue, simply type `python youqueue.py`. To exit, press `Ctrl-C`.

## Usage

Now that you have YouQueue running, you can send an `HTTP GET` request to ask to
download a video:

`curl http://your-host:port/https://www.youtube.com/watch?v=dQw4w9WgXcQ`

You should get back an `HTTP 202` response with an empty body. No, I am not
doing much in the way of error checking or handling. I do print out some
messages which you could write to a log file for troubleshooting.

## Use Cases

On my iPad and iPhone, I built a Shortcut that I can use system-wide to send
URLs to YouQueue. This works great for iOS and iPadOS, but doesn't work yet on
macOS. On my Mac, I use [Hammerspoon](http://www.hammerspoon.org) for
automation, and I added the following customization to my Hammerspoon
configuration to allow me to press `Option-Q` to send the URL in my clipboard to
YouQueue.

```lua
-- Queue Video
hs.hotkey.bind({'option'}, 'q', function()
    local url = hs.pasteboard.getContents()
    hs.alert.show('Attempting to save url ➡️ ' .. url)
    local status, result, headerResponse = hs.http.get(
        'http://192.168.7.20:8781/' .. url
    )
end)
```

The possibilities are endless! Have fun.
