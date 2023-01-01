# titanfall-mod-docs-gen

A python script which generates documentation for [Titanfall 2 + Northstar](https://northstar.tf/).

### TODO:
- Add `@ignore` flag to ignore functions
- Add support for global structs

## Example script file
This action exports only global functions.
```cpp
global function Example

/**
 * Description here. This is pure markdown
 * and can be multiple lines
 * ```cpp
 * // I am a code block
 * ```
 * @param player Short descripiton of this argument
 * @param count Short descripiton of this argument
*/
void function Example( string player, int count ) {
  // ...
}
```

## Example ConVar definition
```json
  {
    "Name": "ExampleConvar",
    "DefaultValue": "1",
    "Description": "Description of what this convar does"
  }
```

## Example github actions setup
```yaml
name: Generate documentation
on: push

jobs:
  docs-gen:
    runs-on: ubuntu-latest
    steps:
      - name: Clone project
        uses: actions/checkout@v2

      - name: Generate docs
        uses: F1F7Y/titanfall-mod-docs-gen@v0

      - name: Push new docs
        working-directory: docs
        run: |
          git config user.name TitanfallDocsGen
          git config user.email "<>"
          git add .
          git diff --quiet HEAD || git commit -m "New docs"
          git push
```
