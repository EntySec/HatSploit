# `post/macos/membrane/trolling/say`

## Description

This module uses system `say` command to say message.

## Verification Steps

1. Start HatSploit
2. Run `exploit/macos/stager/membrane_reverse_tcp` on target
3. Do: `use post/macos/membrane/trolling/say`
4. Do: `set SESSION` to your target session
5. Do: `set MESSAGE` to your message
6. Do: `run`

## Options

| Option    | Default Value  | Required | Description        |
|-----------|----------------|----------|--------------------|
| `MESSAGE` | Hello, membrane! | yes      | Message to say.    |
| `SESSION` | 0              | yes      | Session to run on. |

**MESSAGE**

Variable that contains message you want device to say.

**SESSION**

Variable that contains session id to run post module on it.

## Scenarios

```
(hsf: post: macos/membrane/trolling/say)> run
[*] Sending message to device...
[+] Done saying message!
(hsf: post: macos/membrane/trolling/say)>
```
