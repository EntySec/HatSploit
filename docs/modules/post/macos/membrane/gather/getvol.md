# `post/macos/membrane/gather/getvol`

## Description

This module uses system `osascript` to dump device volume level.

## Verification Steps

1. Start HatSploit
2. Run `exploit/macos/stager/membrane_reverse_tcp` on target
3. Do: `use post/macos/membrane/gather/getvol`
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
(hsf: post: macos/membrane/gather/getvol)> run
[*] Getting device volume level...
[i] Volume Level: 25
(hsf: post: macos/membrane/gather/getvol)>
```
