# queryFile structure
## Background
With "recent" upgrades in openssl to by default not accept legacy renegotiation, some websites don't like this an error out.
The queryFile structure has been updated to allow (on a host-by-host basis) a legacy renegotiation to take place.

## Acceptable File syntax:
```
hostname
hostname,
hostname:port
hostname:port,
hostname,[]
hostname:port,[]
```

In the lines where no `[` or `]` are seen, then it's treated as `None` options provided. i.e. use defaults.

Now in the `[` and `]`, the options that are available to today are:
* `unsafe_legacy` - this allows for legacy renegotiation
* `local_untrusted_allow` - this prevents chain validation. Useful for when websites are misconfigured and presenting the full certificate chain.

To connect to a host with an option configured, these would all be considered valid examples:
```
apple.com,['unsafe_legacy']
apple.com:443,['unsafe_legacy']
```

Another example:
```
apple.com,['local_untrusted_allow']
apple.com:443,['local_untrusted_allow']
apple.com,['unsafe_legacy','local_untrusted_allow']
apple.com:443,['unsafe_legacy','local_untrusted_allow']
```

As you can see, multiple options can be supported on each line.
