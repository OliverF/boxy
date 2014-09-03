boxy
====

Simple two-way UDP packet relay.

# Usage
`boxy.py -i <input port> -a <remote address> -p <remote port>`

- **-i**: Input port the relay listens on (and relays back from)
- **-a**: Remote IP address the relay will send incoming data to
- **-p**: Remote port the relay will send incoming data to

# Example

**Relaying UDP data to remote server B at 192.0.2.1:1234, with the relay running at 192.0.2.0:4321**

![boxy diagram](https://dl.dropboxusercontent.com/u/10518681/boxy.png)

1. Start the relay: `python boxy.py -i 4321 -a 192.0.2.1 -p 1234`

2. Connect to the relay at 192.0.2.0:4321

3. Done! You can send data to the relay and it will be relayed to the remote server, and you will receive the data returned from the remote server back from the relay itself
