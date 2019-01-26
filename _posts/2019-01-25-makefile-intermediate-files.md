I learned about intermediate files in `make`.
Before I explain what they are, let's go over some concepts and terminology of `make`.

Here are some reference documentation:
* [Special Targets](https://www.gnu.org/software/make/manual/html_node/Special-Targets.html)
* [Automatic variables](https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html#Automatic-Variables)

# What are Dependencies
In makefile targets, you can specify dependencies that need to be ran before the recipe begins.
This is a way to abstract and conceptually contain dependencies.

A good example is that you want to run tests, which requires setting up a virtualenv with test tooling.
The recipe for building a debug package or installation would also require the virtualenv dependency.
By abstracting out the virtualenv recipe to its own target, both `test` and `package` targets can depend on and reuse
the same dependency.

# Speeding Up Builds Using Dependencies
`make` dependencies are designed to assist in build optimization.
When building a target, `make` will check the dependency tree to decide which dependencies to build and which can be
skipped.
This is done by comparing file modification timestamps:
* if the dependency has not been modified since the target was last built, there have been no changes to warrant
rebuilding the recipe.
* if the dependency has a newer timestamp than target, the target is stale because there have been changes that are not
in current target

This dependency checking and skipping is purposefully designed to avoid recompiling entire program.
For C programs, only the object files for modified source code are rebuilt.
All other existing objects files can be reused for the final linking step in compilation, greatly speeding things up.

# Phony Targets
A target can be labelled as `.PHONY`, which means that the target does not output a matching physical file.
An example is the `test` target, which is used to trigger test run.
It doesn't create a `test` file.

Because they don't correspond to files on disk, we don't want `make` to check the timestamp for dependency management.
Usually this will work fine because the file will never exist and will always need to be "built".
But if somehow the file were erroneously created, `make` would incorrectly start checking the timestamp.
Things working by coincidence is not great situation to be in.

Marking the target explicitly as `.PHONY` denotes to `make` that it should always run the recipe.
It should ignore any file matching the target name, it was never our intention for the target to output a file.

# Pattern Rules
You can parameterize recipes using patterns.
i.e `test_%` and `venv_%` can be setup such that you can run `make test_py27 test_py36`.
The `%` character is referred to as the "stem" of the pattern and has the `$*` special variable assigned to it.

Examples of things that you might want to parametrize:
* General compiling of source into object files
* Testing different versions of python
* Building binaries for different distributions
* Cross-compiling to different platforms

# Intermediate Files
And now, we get to intermediate files.
Intermediate files are dependencies that don't need to exist before running `make`, and don't need to exist after `make`
finishes running.

C object files are an example of this: you need source files to exist before running `make` and you expect the target
binary to be produced afterwards.
Object files need to only exist "intermediately" as part of the build process.

## What Doesn't Exist Before, Will Not Exist After
`make` follows this conceptual invariant, which helps to explain a lot of design behaviour.
If an intermediate file did not exist before building, it will be cleaned up afterwards.
If it did exist before building, then it will continue to exist afterwards.

## Dependency Handling
Intermediate files are interesting, with respect to dependency management.
Again, it makes much more sense if you internalize the invariant.

If the intermediate dependency does not exist, `make` will continue checking the upstream dependency
(some of which might be regular dependency or phony):
* If upstream dependencies needs to be built, then the intermediate file will also need to be rebuilt.
* If upstream dependencies are up-to-date, then `make` will skip building the intermediate dependency altogether.

If the intermediate dependency exists on disk, then `make` will treat it as a normal file and do modified timestamp
checking.

## How Do You Even Get Intermediate Dependency
Target and dependencies are generally not intermediate.
If you reference the target/dependency explicitly anywhere in the `Makefile`, it will become real. Just like Pinocchio.

If you want to make a target intermediate, mark it as dependency of the special target `.INTERMEDIATE:`.

The other way to get intermediate files was a huge gotcha to me.
It's with patterns.
If you don't reference the dependency in the `Makefile` explicitly, it will end up being intermediate.
i.e. `package_%.zip` will be intermediate. If you add a target or dependency on `package_linux.zip`, then it won't.
This behaviour is unintuitive.

## Argh, I Have Pattern Rules and Don't Want Them To Be Intermediate
You can explicitly add targets for them.
That would make them real, regular targets.

But sometimes that's not feasible, we might be talking about dozens of patterns here.
Mark them as dependency of another special target, `.PRECIOUS`.
This tells `make` to not perform clean up.

**NOTE:** `.PRECIOUS` is the only special target that understands patterns.
Literally the only special target.
This is a gotcha of a gotcha.

## How Are Intermediate Dependencies Handled During Error
If a build is canceled or errors out, what happens?
`make` doesn't have a great user story for handling intermediate files.
It feels like they just slapped on hacks and features until they got something sort of working.

If a build is interrupted, `make` will clean up intermediate files.
Remember, this follows the invariant.
But this is annoying because sometimes a recipe fails because the intermediate dependency was incorrectly built.

It makes sense why `make` wants to clean up files as the default behaviour, even though it would be helpful for
post-mortem debugging.
`make` depends on the file modification timestamp.
A file created during an partial, incomplete build would break this mechanism.
Because it's timestamp is newer than dependency, it would not cause rebuilding as appropriate.

## .SECONDARY
So what if you have an intermediate file that you want to keep after the build but is meaningless as an intermediate
file.
That is, you only want to keep the intermediate file of successful builds.

`.PRECIOUS` will blindly keep all intermediate files, even half-built ones.
`.INTERMEDIATE` will remove all intermediate files.

The answer comes to us in the form of `.SECONDARY` special target. This probably does what you want, all the time:
* If the build is killed (error or ctrl-c), then treat as intermediate file, which means automatic cleanup
* If the build succeeds, treat as precious and keep the artifact.
