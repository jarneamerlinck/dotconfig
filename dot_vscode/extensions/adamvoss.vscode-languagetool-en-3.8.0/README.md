# English Support for LanguageTool

Provides language support for English in when using [LanguageTool for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=adamvoss.vscode-languagetool).  This enables you to do offline grammar checking of English in Visual Studio Code.

## Usage
Set `languageTool.language` to **en** to configure the checking language as English.  You can install as many language support extensions as you like and change between them using this configuration.

## Extension Settings

This extension makes the following values valid for the `languageTool.language` setting:

* en
* en-US
* en-GB
* en-AU
* en-CA
* en-NZ
* en-ZA

## Features
See [LanguageTool for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=adamvoss.vscode-languagetool)

## Requirements
* A compatible version of [LanguageTool for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=adamvoss.vscode-languagetool) must be installed.
  * This package is based on LanguageTool 3.8, so you will need **at least version 3.8.0** of _LanguageTool for Visual Studio Code_.
* Java 8+ is required.

## Versioning

LanguageTool for Visual Studio code has adopted the versioning of its LanguageTool dependency.  For example, if this extension has version 3.8.0 it is powered by LanguageTool 3.8.  vscode-languagetool 3.9.0 would use LanguageTool 3.9.  **The LanguageTool version of this language support extension must match the LanguageTool version of your installed vscode-languagetool extension.**  The easiest way to ensure compatibility is to always update all LanguageTool-related extensions when updating.  We will never have incompatible versions published at the same time.

## Acknowledgments
Please see [ACKNOWLEDGMENTS.md](https://github.com/adamvoss/vscode-languagetool/blob/master/./ACKNOWLEDGMENTS.md)

## Known Issues
Please report issues or submit pull requests on [GitHub](https://github.com/adamvoss/vscode-languagetool).
