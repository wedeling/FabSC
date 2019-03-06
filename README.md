# FabSC
This plugin runs the samples from an EasyVVUQ campaign using FabSim3 via the campaign2emsemble subroutine.

## Installation
Simply type `fab localhost install_plugin:FabSC` anywhere inside your FabSim3 install directory.

## Explanation of files
+ FabSC.py: contains the *sc* subroutine in which the properties per job are specified, e.g. number of cores, memory, wall-time limit etc
+ temples/sc: contains the command-line execution command for a single EasyVVUQ SC sample.

## Detailed Examples

### Executing a single job on localhost
In the examples folder there is a script which runs an EasyVVUQ SC campaign using FabSim3 for a simple advection-diffusion ODE on the localhost. The governing equations are:

![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bdu%7D%7Bdx%7D%20&plus;%20%5Cfrac%7B1%7D%7BPe%7D%5Cfrac%7Bd%5E2u%7D%7Bdx%7D%20%3D%20f)

### Executing a single job on a remote host

1. Ensure the host is defined in machines.yml, and the user login information in `deploy/machines_user.yml`.
2. To run a dummy job, type `fab <machine name> dummy:dummy_test`. This does the following:
  - Copy your job input, which is in `plugins/FabDummy/config_files/dummy_test`, to the remote location specified in the variable `remote_path_template` in `deploy/machines.yml` (not it will substitute in machine-specific variables provided in the same file).
  - Copy the input to the remote results directory.
  - Start the remote job.
3. Your job now likely runs using a scheduler, so your terminal becomes available again. Use `fab <machine> stat` to track its submission status, or `fab <machine> monitor` to poll periodically for the job status.
4. If the stat or monitor commands do not show your job being listed, then your job has finished (successfully or unsuccessfully).
5. You can then fetch the remote data using `fab localhost fetch_results`, and investigate the output as you see fit. Local results are typically locations in the `results/` subdirectory.


### Executing an ensemble job on a remote host

1. Ensure the host is defined in machines.yml, and the user login information in `deploy/machines_user.yml`.
2. To run a dummy job, type `fab <machine name> dummy_ensemble:dummy_test`. This does the following:
  a. Copy your job input, which is in `plugins/FabDummy/config_files/dummy_test`, to the remote location specified in the variable `remote_path_template` in `deploy/machines.yml` (not it will substitute in machine-specific variables provided in the same file).
  b. Copy the input to the remote results directory.
  c. Substitute in the first input file in `plugins/FabDummy/config_files/dummy_test/SWEEP`, renaming it in-place to dummy.txt for the first ensemble run.
  d. Start the remote job.
  e. Repeat b-d for each other base-level file or directory in `plugins/FabDummy/config_files/dummy_test/SWEEP`.
3. Use `fab <machine> stat` to track the submission status of your jobs, or `fab <machine> monitor` to poll periodically for the job status.
4. If the stat or monitor commands do not show any jobs being listed, then all your job has finished (successfully or unsuccessfully).
5. You can then fetch the remote data using `fab localhost fetch_results`, and investigate the output as you see fit. Local results are typically locations in the various `results/` subdirectories.
